-- =========================================================
-- INSURANCE CLAIMS SQL PROJECT
-- Objective: identify factors associated with claim probability
-- =========================================================


-- 1. Global claim rate
SELECT 
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance;


-- 2. Claim rate by customer age group
SELECT 
    CASE 
        WHEN customer_age < 25 THEN 'Under 25'
        WHEN customer_age BETWEEN 25 AND 34 THEN '25-34'
        WHEN customer_age BETWEEN 35 AND 49 THEN '35-49'
        WHEN customer_age BETWEEN 50 AND 64 THEN '50-64'
        ELSE '65+'
    END AS age_group,
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance
GROUP BY age_group
ORDER BY claim_rate_pct DESC;


-- 3. Claim rate by vehicle age
SELECT 
    vehicle_age,
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance
GROUP BY vehicle_age
ORDER BY vehicle_age;


-- 4. Claim rate by region
SELECT 
    region_code,
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance
GROUP BY region_code
ORDER BY claim_rate_pct DESC;


-- 5. Claim rate by number of airbags
SELECT 
    airbags,
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance
GROUP BY airbags
ORDER BY airbags;


-- 6. Most risky vehicle models
SELECT 
    model,
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance
GROUP BY model
HAVING COUNT(*) >= 50
ORDER BY claim_rate_pct DESC;


-- 7. Bonus query: top 3 riskiest regions with ranking
SELECT *
FROM (
    SELECT 
        region_code,
        COUNT(*) AS total_policies,
        ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct,
        RANK() OVER (ORDER BY AVG(claim_status) DESC) AS risk_rank
    FROM insurance
    GROUP BY region_code
) ranked_regions
WHERE risk_rank <= 3
ORDER BY risk_rank;