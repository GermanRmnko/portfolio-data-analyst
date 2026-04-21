import streamlit as st

COLORS = {
    "primary": "#711D1B",
    "secondary": "#BC9558",
    "dark": "#442818",
    "accent": "#9B592A",
    "bg": "#FFE7AB",
    "soft": "#D9C08A",
}


def sql_block(title, business_question, query, insight):
    st.markdown(f"### {title}")
    st.markdown(
        f"""
        <div style="font-size: 20px; line-height: 1.8; color: {COLORS["dark"]};">
        <p><b>Business Question:</b> {business_question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code(query, language="sql")
    st.markdown(
        f"""
        <div style="
            background-color: #f4ddb0;
            border-left: 6px solid {COLORS["primary"]};
            padding: 0.9rem 1rem;
            border-radius: 0.35rem;
            margin: 0.5rem 0 1.2rem 0;
            color: {COLORS["dark"]};
            font-size: 18px;
            line-height: 1.7;
        ">
        <b>Insight:</b> {insight}
        </div>
        """,
        unsafe_allow_html=True
    )


def show():
    st.title(" SQL Project - Insurance Claims")

    sql_page = st.sidebar.radio(
        "SQL Pages",
        [
            "SQL Overview",
            "Business Questions",
            "Example Queries",
            "Key Insights",
        ]
    )
    st.markdown(
    """
    <div style="
        background-color: #f7ead0;
        border-left: 6px solid #9B592A;
        padding: 0.9rem 1rem;
        border-radius: 0.35rem;
        margin: 0.5rem 0 1.2rem 0;
        color: #442818;
        font-size: 18px;
        line-height: 1.7;
    ">
    <b>Note:</b> In this context, "portfolio" refers to the full set of insurance policies included in the dataset, not the project portfolio itself.
    </div>
    """,
    unsafe_allow_html=True
)

    if sql_page == "SQL Overview":
        st.markdown(
            f"""
            <div style="font-size: 28px; line-height: 1.8; color: {COLORS["dark"]};">

            <h2>Project Overview</h2>

            <p>
            This SQL project explores an insurance claims dataset to identify which factors are associated 
            with a higher probability of claim occurrence.
            </p>

            <p>
            The goal is not only to write SQL queries, but also to answer concrete business questions 
            and translate raw data into short, actionable insights.
            </p>

            <h2>Dataset</h2>

            <p>
            The dataset includes customer and vehicle-related variables such as customer age, vehicle age, 
            vehicle model, region, number of airbags, and claim status.
            </p>

            <h2>SQL Objectives</h2>

            <ul>
                <li>Measure the global claim rate</li>
                <li>Compare claim rates across customer segments</li>
                <li>Assess vehicle-related risk factors</li>
                <li>Identify high-risk regions and models</li>
                <li>Translate SQL output into business interpretation</li>
            </ul>

            </div>
            """,
            unsafe_allow_html=True
        )

    elif sql_page == "Business Questions":
        def premium_block(title, question, query, insight):
            st.markdown(
            f"""
            <div style="
                background-color: white;
                padding: 1.2rem 1.4rem;
                border-radius: 0.6rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 14px rgba(0,0,0,0.08);
                border-left: 6px solid {COLORS["primary"]};
            ">

            <h3 style="color: {COLORS["primary"]}; margin-bottom: 0.5rem;">{title}</h3>

            <p style="font-size:18px; color:{COLORS["dark"]};">
            <b>Business Question:</b> {question}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )
           
        st.markdown(
        f"""
        <div style="font-size: 28px; line-height: 1.9; color: {COLORS["dark"]};">

        <h2>Business Questions</h2>

        <p>
        This analysis aims to understand which factors are associated with a higher probability of insurance claims.
        The following business questions guide the SQL analysis:
        </p>

        <p><b>1.</b> What percentage of customers filed a claim?</p>

        <p><b>2.</b> Does claim probability vary by customer age?</p>

        <p><b>3.</b> Does vehicle age influence claim rate?</p>

        <p><b>4.</b> Are some regions associated with higher claim rates?</p>

        <p><b>5.</b> Do safety features such as airbags reduce claim probability?</p>

        <p><b>6.</b> Which vehicle models show the highest claim rates?</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    elif sql_page == "Example Queries":
        query_1 = """
SELECT 
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance;
"""

        query_2 = """
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
"""

        query_3 = """
SELECT 
    vehicle_age,
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance
GROUP BY vehicle_age
ORDER BY vehicle_age;
"""

        query_4 = """
SELECT 
    region_code,
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance
GROUP BY region_code
ORDER BY claim_rate_pct DESC;
"""

        query_5 = """
SELECT 
    airbags,
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance
GROUP BY airbags
ORDER BY airbags;
"""

        query_6 = """
SELECT 
    model,
    COUNT(*) AS total_policies,
    SUM(claim_status) AS total_claims,
    ROUND(AVG(claim_status) * 100, 2) AS claim_rate_pct
FROM insurance
GROUP BY model
HAVING COUNT(*) >= 50
ORDER BY claim_rate_pct DESC;
"""

        st.markdown("## Example Queries")

        sql_block(
            "1. Global Claim Rate",
            "What is the overall claim rate in the portfolio?",
            query_1,
            "This query establishes the baseline risk level of the portfolio and provides a reference point for all segment comparisons."
        )

        sql_block(
            "2. Claim Rate by Customer Age",
            "Does claim probability vary by customer age?",
            query_2,
            "Younger or older customer segments may present different claim rates, which can help identify higher-risk profiles."
        )

        sql_block(
            "3. Claim Rate by Vehicle Age",
            "Does vehicle age influence claim rate?",
            query_3,
            "Older vehicles may be associated with higher claim rates, suggesting a potential impact of wear, maintenance, or equipment level."
        )

        sql_block(
            "4. Claim Rate by Region",
            "Are some regions associated with higher risk?",
            query_4,
            "Regional differences may reveal distinct driving environments or exposure patterns that affect claim probability."
        )

        sql_block(
            "5. Claim Rate by Airbags",
            "Do airbags appear to reduce claim probability?",
            query_5,
            "This query explores whether better-equipped vehicles are associated with lower claim rates."
        )

        sql_block(
            "6. Most Risky Vehicle Models",
            "Which vehicle models show the highest claim rates?",
            query_6,
            "Some models may consistently show higher claim rates, which can indicate a structural risk pattern."
        )

    elif sql_page == "Key Insights":

        st.markdown(
        f"""
        <div style="font-size: 28px; line-height: 1.8; color: {COLORS["dark"]};">

        <h2>Key Insights</h2>

        <p>
        <b>1. Overall claim rate:</b><br>
        Around X% of customers filed a claim, providing a baseline level of risk across the dataset.
        </p>

        <p>
        <b>2. Customer age:</b><br>
        Younger customers tend to show higher claim rates, suggesting a higher-risk profile for this segment.
        </p>

        <p>
        <b>3. Vehicle age:</b><br>
        Claim rates increase with vehicle age, indicating that older vehicles may be more prone to incidents.
        </p>

        <p>
        <b>4. Regional differences:</b><br>
        Significant variations appear across regions, suggesting that claim risk is not evenly distributed geographically.
        </p>

        <p>
        <b>5. Safety features (airbags):</b><br>
        Vehicles with more airbags tend to show lower claim rates, suggesting a potential protective effect.
        </p>

        <p>
        <b>6. Vehicle models:</b><br>
        Some models consistently show higher claim rates, indicating potential structural differences in risk.
        </p>

        <p>
        <b>Conclusion:</b><br>
        These results suggest that both customer and vehicle characteristics play a key role in claim probability, 
        and could be used to improve risk segmentation and pricing strategies.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
        
        