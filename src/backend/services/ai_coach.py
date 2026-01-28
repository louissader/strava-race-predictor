"""
AI Running Coach Service
Provides personalized training advice using AWS Bedrock (Claude)
"""

import boto3
import json
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Get project root (3 levels up from this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))


def get_bedrock_client():
    """Initialize AWS Bedrock client"""
    region = os.getenv('AWS_REGION', 'us-east-1')
    profile = os.getenv('AWS_PROFILE')

    try:
        if profile:
            session = boto3.Session(profile_name=profile)
            return session.client('bedrock-runtime', region_name=region)
        else:
            return boto3.client('bedrock-runtime', region_name=region)
    except Exception as e:
        print(f"Error initializing Bedrock client: {e}")
        return None


def build_training_context(activities_df, race_df, predictions):
    """
    Aggregates user's training data for LLM context:
    - Recent 30/60/90 day stats (distance, runs, avg pace)
    - Current race predictions (5K, 10K, Half, Marathon)
    - Training trends (improving/declining/plateau)
    - Recent activities (last 7-10 runs with details)
    - Weekly patterns (preferred days, time of day)
    """
    runs = activities_df[activities_df['type'] == 'Run'].copy()

    if len(runs) == 0:
        return {"error": "No running data available"}

    # Unit conversions
    KM_TO_MILES = 0.621371
    M_TO_FT = 3.28084

    # Current date for calculations (timezone-aware to match activity data)
    now = pd.Timestamp.now(tz='UTC')

    # Recent stats for different periods
    def get_period_stats(days):
        cutoff = now - timedelta(days=days)
        recent = runs[runs['start_date'] >= cutoff]
        if len(recent) == 0:
            return None

        total_distance_mi = recent['distance_km'].sum() * KM_TO_MILES
        avg_pace_min_per_mi = recent['pace_min_per_km'].mean() / KM_TO_MILES

        return {
            'runs': int(len(recent)),
            'distance_mi': round(total_distance_mi, 1),
            'avg_pace_min_per_mi': round(avg_pace_min_per_mi, 2),
            'total_elevation_ft': round(recent['total_elevation_gain'].sum() * M_TO_FT, 0),
            'longest_run_mi': round(recent['distance_km'].max() * KM_TO_MILES, 1),
            'avg_run_mi': round(recent['distance_km'].mean() * KM_TO_MILES, 1)
        }

    stats_30d = get_period_stats(30)
    stats_60d = get_period_stats(60)
    stats_90d = get_period_stats(90)

    # Weekly average (past 12 weeks)
    stats_84d = get_period_stats(84)
    weekly_avg_mi = stats_84d['distance_mi'] / 12 if stats_84d else 0
    weekly_avg_runs = stats_84d['runs'] / 12 if stats_84d else 0

    # Last 10 activities with details
    recent_runs = runs.nlargest(10, 'start_date')[
        ['name', 'distance_km', 'pace_min_per_km', 'moving_time_min', 'start_date', 'total_elevation_gain']
    ].copy()

    last_activities = []
    for _, run in recent_runs.iterrows():
        last_activities.append({
            'name': run['name'],
            'date': run['start_date'].strftime('%Y-%m-%d'),
            'distance_mi': round(run['distance_km'] * KM_TO_MILES, 1),
            'pace_min_per_mi': round(run['pace_min_per_km'] / KM_TO_MILES, 2),
            'duration_min': round(run['moving_time_min'], 0),
            'elevation_ft': round(run['total_elevation_gain'] * M_TO_FT, 0)
        })

    # Training trend analysis
    if stats_30d and stats_90d:
        recent_weekly = stats_30d['distance_mi'] / 4
        overall_weekly = stats_90d['distance_mi'] / 12

        if recent_weekly > overall_weekly * 1.1:
            trend = "increasing"
            trend_description = f"Your training volume has increased. Recent weekly average ({recent_weekly:.1f} mi/week) is higher than your 12-week average ({overall_weekly:.1f} mi/week)."
        elif recent_weekly < overall_weekly * 0.9:
            trend = "decreasing"
            trend_description = f"Your training volume has decreased. Recent weekly average ({recent_weekly:.1f} mi/week) is lower than your 12-week average ({overall_weekly:.1f} mi/week)."
        else:
            trend = "stable"
            trend_description = f"Your training volume is stable at about {overall_weekly:.1f} miles per week."
    else:
        trend = "unknown"
        trend_description = "Not enough data to determine training trend."

    # Weekly patterns
    runs['day_of_week'] = runs['start_date'].dt.day_name()
    runs['hour'] = runs['start_date'].dt.hour

    day_counts = runs['day_of_week'].value_counts()
    favorite_days = day_counts.head(3).index.tolist()

    hour_counts = runs['hour'].value_counts()
    peak_hour = hour_counts.idxmax()
    if peak_hour < 12:
        preferred_time = "morning"
    elif peak_hour < 17:
        preferred_time = "afternoon"
    else:
        preferred_time = "evening"

    # Overall stats
    total_runs = len(runs)
    total_distance_mi = runs['distance_km'].sum() * KM_TO_MILES
    first_run = runs['start_date'].min().strftime('%Y-%m-%d')
    last_run = runs['start_date'].max().strftime('%Y-%m-%d')

    # Format race predictions for context
    prediction_summary = {}
    for distance, pred in predictions.items():
        if pred.get('has_model'):
            prediction_summary[distance] = {
                'best_time_min': pred['best_time_min'],
                'num_races': pred['num_races'],
                'recent_time_min': pred.get('recent_time_min')
            }

    context = {
        'total_runs': total_runs,
        'total_distance_mi': round(total_distance_mi, 0),
        'running_since': first_run,
        'last_run_date': last_run,
        'weekly_avg_mi': round(weekly_avg_mi, 1),
        'weekly_avg_runs': round(weekly_avg_runs, 1),
        'stats_30d': stats_30d,
        'stats_60d': stats_60d,
        'stats_90d': stats_90d,
        'trend': trend,
        'trend_description': trend_description,
        'predictions': prediction_summary,
        'last_activities': last_activities,
        'favorite_days': favorite_days,
        'preferred_time': preferred_time
    }

    return context


def format_pace(pace_min):
    """Format pace from decimal minutes to MM:SS"""
    if not pace_min or pace_min <= 0:
        return "N/A"
    minutes = int(pace_min)
    seconds = int((pace_min - minutes) * 60)
    return f"{minutes}:{seconds:02d}"


def format_time(minutes):
    """Format time from minutes to HH:MM:SS or MM:SS"""
    if not minutes or minutes <= 0:
        return "N/A"
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    secs = int((minutes % 1) * 60)
    if hours > 0:
        return f"{hours}:{mins:02d}:{secs:02d}"
    return f"{mins}:{secs:02d}"


def get_system_prompt(context):
    """
    Returns coaching system prompt with user's training data injected
    """
    # Format predictions for prompt
    pred_lines = []
    for distance, pred in context.get('predictions', {}).items():
        time_str = format_time(pred['best_time_min'])
        pred_lines.append(f"  - {distance}: {time_str} (based on {pred['num_races']} races)")
    predictions_text = "\n".join(pred_lines) if pred_lines else "  - No race data available yet"

    # Format recent activities
    activity_lines = []
    for act in context.get('last_activities', [])[:7]:
        pace_str = format_pace(act['pace_min_per_mi'])
        activity_lines.append(
            f"  - {act['date']}: {act['name']} - {act['distance_mi']} mi @ {pace_str}/mi"
        )
    activities_text = "\n".join(activity_lines) if activity_lines else "  - No recent activities"

    # 30-day stats
    stats_30d = context.get('stats_30d', {}) or {}
    pace_30d = format_pace(stats_30d.get('avg_pace_min_per_mi', 0))

    system_prompt = f"""You are an expert running coach with 20+ years of experience coaching recreational to elite runners. You have access to this athlete's complete training history and current fitness level.

## Athlete Profile
- Total runs: {context.get('total_runs', 0)}
- Total distance: {context.get('total_distance_mi', 0)} miles
- Running since: {context.get('running_since', 'N/A')}
- Weekly average: {context.get('weekly_avg_mi', 0)} miles across {context.get('weekly_avg_runs', 0)} runs
- Preferred running time: {context.get('preferred_time', 'unknown')}
- Favorite running days: {', '.join(context.get('favorite_days', ['unknown']))}

## Current Fitness (Race Predictions)
{predictions_text}

## Recent Training (Last 30 Days)
- Total distance: {stats_30d.get('distance_mi', 0)} miles
- Number of runs: {stats_30d.get('runs', 0)}
- Average pace: {pace_30d} /mi
- Longest run: {stats_30d.get('longest_run_mi', 0)} miles

## Training Trend
{context.get('trend_description', 'No trend data available')}

## Recent Activities
{activities_text}

## Coaching Guidelines
- Follow the 80/20 rule: 80% easy running, 20% harder efforts (tempo, intervals, races)
- Never increase weekly mileage more than 10% per week
- Include rest days and recovery weeks (every 3-4 weeks, reduce volume by 30-40%)
- Be encouraging but realistic about goals and timelines
- Reference specific data from their training when giving advice
- Suggest specific workouts when appropriate (e.g., "Try 4x800m at {pace}")
- Consider injury prevention - watch for sudden mileage increases
- Tailor advice to their experience level and current fitness

When discussing times and paces:
- Use minutes:seconds format (e.g., 7:30/mi not 7.5 min/mi)
- Be specific about workout intensities (easy, tempo, threshold, interval, race pace)

Keep responses conversational but informative. Reference their actual training data to make advice personal and actionable."""

    return system_prompt


def chat(user_message, conversation_history, context):
    """
    Sends message to Bedrock Claude with training context (non-streaming)

    Args:
        user_message: The user's new message
        conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
        context: Training context from build_training_context()

    Returns:
        Coach's response string
    """
    client = get_bedrock_client()
    if not client:
        return "Sorry, I'm having trouble connecting to the AI service. Please check your AWS credentials."

    system_prompt = get_system_prompt(context)

    # Build messages array
    messages = []
    for msg in conversation_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add new user message
    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "system": system_prompt,
                "messages": messages
            })
        )

        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']

    except Exception as e:
        error_msg = str(e)
        if 'AccessDeniedException' in error_msg:
            return "Access denied to AWS Bedrock. Please ensure you have the Claude model enabled in your AWS Bedrock console and proper IAM permissions."
        elif 'ResourceNotFoundException' in error_msg:
            return "The Claude model is not available in your AWS region. Please check that Claude 3 Sonnet is enabled in us-east-1."
        else:
            print(f"Bedrock API error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"


def chat_stream(user_message, conversation_history, context):
    """
    Sends message to Bedrock Claude with streaming response

    Args:
        user_message: The user's new message
        conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
        context: Training context from build_training_context()

    Yields:
        Tokens as they are received from Bedrock
    """
    client = get_bedrock_client()
    if not client:
        yield {"type": "error", "text": "Sorry, I'm having trouble connecting to the AI service. Please check your AWS credentials."}
        return

    system_prompt = get_system_prompt(context)

    # Build messages array
    messages = []
    for msg in conversation_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add new user message
    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.invoke_model_with_response_stream(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "system": system_prompt,
                "messages": messages
            })
        )

        # Process the streaming response
        for event in response.get('body'):
            chunk = json.loads(event['chunk']['bytes'].decode('utf-8'))

            if chunk['type'] == 'content_block_delta':
                delta = chunk.get('delta', {})
                if delta.get('type') == 'text_delta':
                    text = delta.get('text', '')
                    if text:
                        yield {"type": "token", "text": text}

            elif chunk['type'] == 'message_stop':
                yield {"type": "done"}

    except Exception as e:
        error_msg = str(e)
        if 'AccessDeniedException' in error_msg:
            yield {"type": "error", "text": "Access denied to AWS Bedrock. Please ensure you have the Claude model enabled in your AWS Bedrock console and proper IAM permissions."}
        elif 'ResourceNotFoundException' in error_msg:
            yield {"type": "error", "text": "The Claude model is not available in your AWS region. Please check that Claude 3 Sonnet is enabled in us-east-1."}
        else:
            print(f"Bedrock API streaming error: {e}")
            yield {"type": "error", "text": f"Sorry, I encountered an error: {str(e)}"}


def generate_training_plan(goal_race, goal_time, weeks, context):
    """
    Generates a structured training plan based on goal race and current fitness

    Args:
        goal_race: Target race distance (5K, 10K, Half Marathon, Marathon)
        goal_time: Goal time in "MM:SS" or "HH:MM:SS" format
        weeks: Number of weeks until the race
        context: Training context from build_training_context()

    Returns:
        Dictionary with plan details
    """
    client = get_bedrock_client()
    if not client:
        return {"error": "Failed to connect to AI service"}

    # Get current prediction for this distance
    current_prediction = None
    predictions = context.get('predictions', {})
    if goal_race in predictions:
        current_prediction = format_time(predictions[goal_race]['best_time_min'])

    system_prompt = get_system_prompt(context)

    plan_prompt = f"""Based on this athlete's current fitness, create a {weeks}-week training plan to prepare for a {goal_race} race with a goal time of {goal_time}.

{"Current " + goal_race + " prediction: " + current_prediction if current_prediction else "No current " + goal_race + " prediction available."}

Current weekly average: {context.get('weekly_avg_mi', 0)} miles

Please provide a structured training plan in the following JSON format:
{{
    "summary": "Brief overview of the plan approach",
    "weekly_target_start": "Starting weekly mileage",
    "weekly_target_peak": "Peak weekly mileage",
    "key_workouts": ["List of key workout types you'll incorporate"],
    "weeks": [
        {{
            "week": 1,
            "focus": "Base building / Speed / Taper etc.",
            "total_miles": 25,
            "days": [
                {{"day": "Monday", "workout": "Rest"}},
                {{"day": "Tuesday", "workout": "Easy 4 miles"}},
                {{"day": "Wednesday", "workout": "5x800m @ 3:30 with 400m jog recovery"}},
                {{"day": "Thursday", "workout": "Easy 5 miles"}},
                {{"day": "Friday", "workout": "Rest or cross-train"}},
                {{"day": "Saturday", "workout": "Long run 8 miles @ easy pace"}},
                {{"day": "Sunday", "workout": "Recovery 3 miles"}}
            ]
        }}
    ],
    "race_day_tips": "Brief race day strategy",
    "notes": "Any important notes or warnings"
}}

Important guidelines:
- Start from their current fitness level (~{context.get('weekly_avg_mi', 0)} mi/week)
- Don't increase weekly volume more than 10% per week
- Include a recovery week every 3-4 weeks (reduce volume 30-40%)
- Taper for the final 1-2 weeks depending on race distance
- Be realistic about whether the goal is achievable in the timeframe
- Include their preferred running days: {', '.join(context.get('favorite_days', ['any days']))}

Return ONLY the JSON object, no additional text."""

    try:
        response = client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "system": system_prompt,
                "messages": [{"role": "user", "content": plan_prompt}]
            })
        )

        response_body = json.loads(response['body'].read())
        plan_text = response_body['content'][0]['text']

        # Parse JSON from response
        try:
            # Find JSON in response (in case there's extra text)
            start = plan_text.find('{')
            end = plan_text.rfind('}') + 1
            if start >= 0 and end > start:
                plan_json = json.loads(plan_text[start:end])
                return {
                    "plan": plan_json,
                    "current_prediction": current_prediction,
                    "goal_race": goal_race,
                    "goal_time": goal_time,
                    "weeks": weeks
                }
            else:
                return {"error": "Could not parse training plan", "raw_response": plan_text}
        except json.JSONDecodeError as e:
            return {"error": f"JSON parse error: {e}", "raw_response": plan_text}

    except Exception as e:
        print(f"Bedrock API error: {e}")
        return {"error": str(e)}


def get_context_summary(context):
    """
    Returns a simplified context summary for the frontend
    """
    stats_30d = context.get('stats_30d', {}) or {}

    # Format predictions
    predictions = {}
    for distance, pred in context.get('predictions', {}).items():
        predictions[distance] = {
            'time': format_time(pred['best_time_min']),
            'num_races': pred['num_races']
        }

    return {
        'total_runs': context.get('total_runs', 0),
        'total_miles': context.get('total_distance_mi', 0),
        'weekly_avg_miles': context.get('weekly_avg_mi', 0),
        'last_30_days': {
            'runs': stats_30d.get('runs', 0),
            'miles': stats_30d.get('distance_mi', 0),
            'avg_pace': format_pace(stats_30d.get('avg_pace_min_per_mi', 0))
        },
        'trend': context.get('trend', 'unknown'),
        'trend_description': context.get('trend_description', ''),
        'predictions': predictions,
        'last_run': context.get('last_run_date', 'N/A')
    }
