"""
Train machine learning models to predict race times
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from utils.data_preprocessing import load_activities, create_race_dataset, prepare_features_for_ml

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def train_and_evaluate_models(X, y, feature_names):
    """
    Train multiple models and compare performance

    Args:
        X: Feature matrix
        y: Target values
        feature_names: Names of features

    Returns:
        Best model and results dictionary
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define models to try
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=5),
        'Ridge Regression': Ridge(alpha=1.0),
        'Lasso Regression': Lasso(alpha=0.1),
    }

    results = {}

    print("\nTraining and evaluating models...")
    print("=" * 70)

    for name, model in models.items():
        # Train model
        model.fit(X_train_scaled, y_train)

        # Predictions
        y_train_pred = model.predict(X_train_scaled)
        y_test_pred = model.predict(X_test_scaled)

        # Metrics
        train_mae = mean_absolute_error(y_train, y_train_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)

        # Cross-validation
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=min(5, len(X_train)),
                                     scoring='neg_mean_absolute_error')
        cv_mae = -cv_scores.mean()

        results[name] = {
            'model': model,
            'train_mae': train_mae,
            'test_mae': test_mae,
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'cv_mae': cv_mae,
            'y_test': y_test,
            'y_pred': y_test_pred
        }

        print(f"\n{name}:")
        print(f"  Train MAE: {train_mae:.2f} min | Test MAE: {test_mae:.2f} min | CV MAE: {cv_mae:.2f} min")
        print(f"  Train RMSE: {train_rmse:.2f} min | Test RMSE: {test_rmse:.2f} min")
        print(f"  Train R²: {train_r2:.3f} | Test R²: {test_r2:.3f}")

    # Select best model based on test MAE
    best_model_name = min(results.keys(), key=lambda k: results[k]['test_mae'])
    best_model = results[best_model_name]['model']

    print(f"\n{'=' * 70}")
    print(f"Best Model: {best_model_name}")
    print(f"Test MAE: {results[best_model_name]['test_mae']:.2f} minutes")
    print(f"Test RMSE: {results[best_model_name]['test_rmse']:.2f} minutes")
    print(f"Test R²: {results[best_model_name]['test_r2']:.3f}")

    return best_model, scaler, results, feature_names

def plot_model_comparison(results, distance, save_path='plots/model_comparison.png'):
    """Plot comparison of model performance"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # MAE comparison
    model_names = list(results.keys())
    test_maes = [results[m]['test_mae'] for m in model_names]
    cv_maes = [results[m]['cv_mae'] for m in model_names]

    x = np.arange(len(model_names))
    width = 0.35

    axes[0].bar(x - width/2, test_maes, width, label='Test MAE', alpha=0.8)
    axes[0].bar(x + width/2, cv_maes, width, label='CV MAE', alpha=0.8)
    axes[0].set_xlabel('Model')
    axes[0].set_ylabel('Mean Absolute Error (minutes)')
    axes[0].set_title(f'Model Performance Comparison - {distance}')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(model_names, rotation=45, ha='right')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # R² comparison
    test_r2s = [results[m]['test_r2'] for m in model_names]

    axes[1].bar(model_names, test_r2s, alpha=0.8, color='green')
    axes[1].set_xlabel('Model')
    axes[1].set_ylabel('R² Score')
    axes[1].set_title(f'R² Score Comparison - {distance}')
    axes[1].set_xticklabels(model_names, rotation=45, ha='right')
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=0, color='r', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nModel comparison plot saved to {save_path}")
    plt.close()

def plot_predictions(results, best_model_name, distance, save_path='plots/predictions.png'):
    """Plot actual vs predicted race times"""
    y_test = results[best_model_name]['y_test']
    y_pred = results[best_model_name]['y_pred']

    plt.figure(figsize=(10, 8))
    plt.scatter(y_test, y_pred, alpha=0.6, s=100)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Perfect Prediction')

    plt.xlabel('Actual Race Time (minutes)', fontsize=12)
    plt.ylabel('Predicted Race Time (minutes)', fontsize=12)
    plt.title(f'Actual vs Predicted Race Times - {distance}\n{best_model_name}', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    # Add error margin lines
    mae = results[best_model_name]['test_mae']
    plt.fill_between([y_test.min(), y_test.max()],
                      [y_test.min() - mae, y_test.max() - mae],
                      [y_test.min() + mae, y_test.max() + mae],
                      alpha=0.2, label=f'±{mae:.2f} min')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Predictions plot saved to {save_path}")
    plt.close()

def plot_feature_importance(model, feature_names, distance, save_path='plots/feature_importance.png'):
    """Plot feature importance for tree-based models"""
    if not hasattr(model, 'feature_importances_'):
        print("Model does not have feature_importances_ attribute")
        return

    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:15]  # Top 15 features

    plt.figure(figsize=(12, 8))
    plt.barh(range(len(indices)), importances[indices], alpha=0.8)
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel('Feature Importance', fontsize=12)
    plt.title(f'Top 15 Most Important Features - {distance}', fontsize=14)
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Feature importance plot saved to {save_path}")
    plt.close()

def train_for_distance(race_df, distance):
    """Train model for a specific race distance"""
    print(f"\n{'=' * 70}")
    print(f"TRAINING MODEL FOR {distance}")
    print(f"{'=' * 70}")

    # Prepare features
    X, y, feature_names = prepare_features_for_ml(race_df, distance)

    if X is None or len(X) < 5:
        print(f"Not enough data to train model for {distance}")
        return None

    print(f"\nDataset size: {len(X)} races")
    print(f"Number of features: {len(feature_names)}")
    print(f"Race time range: {y.min():.2f} - {y.max():.2f} minutes")

    # Train models
    best_model, scaler, results, feature_names = train_and_evaluate_models(X, y, feature_names)

    # Get best model name
    best_model_name = min(results.keys(), key=lambda k: results[k]['test_mae'])

    # Create plots
    os.makedirs('plots', exist_ok=True)
    plot_model_comparison(results, distance, f'plots/model_comparison_{distance.replace(" ", "_")}.png')
    plot_predictions(results, best_model_name, distance, f'plots/predictions_{distance.replace(" ", "_")}.png')
    plot_feature_importance(best_model, feature_names, distance, f'plots/feature_importance_{distance.replace(" ", "_")}.png')

    # Save model
    model_data = {
        'model': best_model,
        'scaler': scaler,
        'feature_names': feature_names,
        'distance': distance,
        'test_mae': results[best_model_name]['test_mae'],
        'test_r2': results[best_model_name]['test_r2']
    }

    os.makedirs('models', exist_ok=True)
    model_path = f'models/{distance.replace(" ", "_")}_model.joblib'
    joblib.dump(model_data, model_path)
    print(f"\nModel saved to {model_path}")

    return model_data

def main():
    """Main training pipeline"""
    print("Race Time Prediction Model Training")
    print("=" * 70)

    # Load and preprocess data
    print("\nLoading activities...")
    activities_df = load_activities()

    print("\nCreating race dataset...")
    race_df = create_race_dataset(activities_df)

    if race_df is None:
        print("Failed to create race dataset")
        return

    # Train models for each distance
    distances = race_df['race_distance'].unique()
    print(f"\nAvailable race distances: {distances}")

    models = {}
    for distance in distances:
        if pd.notna(distance):
            model_data = train_for_distance(race_df, distance)
            if model_data:
                models[distance] = model_data

    print(f"\n{'=' * 70}")
    print("TRAINING COMPLETE")
    print(f"{'=' * 70}")
    print(f"\nTrained models for {len(models)} distances:")
    for distance, model_data in models.items():
        print(f"  {distance}:")
        print(f"    Test MAE: {model_data['test_mae']:.2f} minutes")
        print(f"    Test R²: {model_data['test_r2']:.3f}")

if __name__ == "__main__":
    main()
