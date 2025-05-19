import numpy as np

def dp_mean(ages, epsilon, A_max=120):
    """
    Compute an epsilon-differentially-private mean of the input ages.
    
    Parameters:
      ages    - list or numpy array of numeric ages (each in [0, A_max])
      epsilon - privacy budget (>0)
      A_max   - maximum possible age (default 120)
    
    Returns:
      A tuple (noisy_mean, noise) where:
        noisy_mean = true_mean + LaplaceNoise
        noise      = the sampled Laplace noise
    """
    n = len(ages)
    if n == 0:
        raise ValueError("Age list must be non-empty")
    true_mean = np.mean(ages)
    
    # Sensitivity of the mean query over [0, A_max]
    delta_f = A_max / n
    
    # Scale for Laplace noise
    b = delta_f / epsilon
    
    # Sample Laplace noise
    noise = np.random.laplace(loc=0.0, scale=b)
    
    return true_mean + noise, noise

# Demo
if __name__ == "__main__":
    # Example data
    survey_ages = [23, 37, 29, 41, 55, 62, 19, 47, 30, 28]
    eps = 0.5
    
    noisy_avg, noise = dp_mean(survey_ages, eps)
    print(f"True average: {np.mean(survey_ages):.2f}")
    print(f"Noisy average (ε={eps}): {noisy_avg:.2f}")
    print(f"Added noise: {noise:.2f}")
