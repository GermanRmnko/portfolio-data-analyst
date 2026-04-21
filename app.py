import os
import insurance_sql
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="E-commerce Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "primary": "#711D1B",
    "secondary": "#BC9558",
    "dark": "#442818",
    "accent": "#9B592A",
    "bg": "#FFE7AB",
    "soft": "#D9C08A",
}

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {COLORS["bg"]};
        color: {COLORS["dark"]};
    }}

    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}

    [data-testid="stHeader"] button {{
        color: #711D1B !important;
    }}

    [data-testid="stHeader"] button svg {{
        fill: #711D1B !important;
        stroke: #711D1B !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: #711D1B;
    }}

    h1, h2, h3, h4 {{
        color: {COLORS["dark"]};
    }}

    .insight-box {{
        background-color: #f4ddb0;
        border-left: 6px solid {COLORS["primary"]};
        padding: 0.9rem 1rem;
        border-radius: 0.35rem;
        margin: 0.4rem 0 1rem 0;
        color: {COLORS["dark"]};
    }}

    .note-box {{
        background-color: #f7ead0;
        border-left: 6px solid {COLORS["accent"]};
        padding: 0.9rem 1rem;
        border-radius: 0.35rem;
        margin: 0.4rem 0 1rem 0;
        color: {COLORS["dark"]};
    }}

    [data-testid="stMetricValue"] {{
        color: #711D1B;
    }}

    [data-testid="stMetricLabel"] {{
        color: #442818;
    }}

    div[data-baseweb="select"] {{
        cursor: pointer !important;
    }}

    div[data-baseweb="select"] * {{
        cursor: pointer !important;
    }}

    ul[role="listbox"] {{
        cursor: pointer !important;
    }}

    ul[role="listbox"] li {{
        cursor: pointer !important;
    }}

    ul[role="listbox"] li * {{
        cursor: pointer !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def style_ax(ax):
    ax.set_facecolor(COLORS["bg"])
    ax.grid(axis="y", color=COLORS["accent"], alpha=0.18)
    ax.tick_params(colors=COLORS["dark"])
    for spine in ax.spines.values():
        spine.set_color(COLORS["soft"])
    ax.title.set_color(COLORS["dark"])
    ax.xaxis.label.set_color(COLORS["dark"])
    ax.yaxis.label.set_color(COLORS["dark"])


def money_formatter(x, _):
    return f"{x:,.0f}"


def make_fig(figsize=(7.2, 4.2)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(COLORS["bg"])
    style_ax(ax)
    fig.tight_layout()
    return fig, ax


def show_fig(fig):
    c1, c2, c3 = st.columns([0.5, 3, 0.5])
    with c2:
        st.pyplot(fig, use_container_width=False)


def nearest_rate(x, allowed):
    return allowed[abs(allowed - x).argmin()]


def section_title(title):
    st.markdown(f"## {title}")


def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def note(text):
    st.markdown(f'<div class="note-box">{text}</div>', unsafe_allow_html=True)


@st.cache_data
def load_data():
    candidates = [
        "ecommerce_customer_behavior_dataset_v2.csv",
        "./ecommerce_customer_behavior_dataset_v2.csv",
        "/mnt/data/ecommerce_customer_behavior_dataset_v2.csv",
    ]
    for path in candidates:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    else:
        raise FileNotFoundError(
            "CSV file not found. Put 'ecommerce_customer_behavior_dataset_v2.csv' in the same folder as app.py."
        )

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Discount_Rate"] = df["Discount_Amount"] / (df["Unit_Price"] * df["Quantity"])
    df["Discount_Rate"] = df["Discount_Rate"].fillna(0)

    allowed_rates = pd.Series([0.00, 0.05, 0.10, 0.15, 0.20, 0.25], dtype=float)
    df["Discount_Rate_Clean"] = df["Discount_Rate"].apply(lambda x: nearest_rate(x, allowed_rates))
    df["Discount_Label"] = (df["Discount_Rate_Clean"] * 100).round().astype(int).astype(str) + "%"

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[18, 25, 35, 45, 55, 65],
        labels=["18-25", "25-35", "35-45", "45-55", "55-65"],
        include_lowest=True
    )

    df["Session_Group"] = pd.cut(
        df["Session_Duration_Minutes"],
        bins=[0, 5, 10, 15, 20, 100],
        labels=["0-5", "5-10", "10-15", "15-20", "20+"],
        include_lowest=True
    )

    df["Pages_Group"] = pd.cut(
        df["Pages_Viewed"],
        bins=[0, 5, 10, 15, 20],
        labels=["0-5", "5-10", "10-15", "15-20"],
        include_lowest=True
    )

    df["Delivery_Group"] = pd.cut(
        df["Delivery_Time_Days"],
        bins=[0, 2, 4, 6, 8, 10],
        labels=["1-2d", "3-4d", "5-6d", "7-8d", "9-10d"],
        include_lowest=True
    )

    return df


df = load_data()

st.sidebar.title("Navigation")

section = st.sidebar.selectbox(
    "Go to",
    ["Home", "Python E-commerce Data Analysis", "SQL Projects", "Power BI"]
)

page = "Home"

if section == "Python E-commerce Data Analysis":
    page = st.sidebar.radio(
        "Pages",
        [
            "Overview",
            "Average Order Value",
            "Discounts",
            "Customer Value",
            "Categories",
            "User Behavior",
            "Age & Categories",
            "Geography",
            "Delivery & Satisfaction",
            "Conclusion",
            "Next Step With Real Data",
        ],
    )

elif section == "Power BI":
    page = st.sidebar.radio(
        "Pages",
        [
            "Dashboard Overview",
            "Key Metrics",
            "Insights",
        ],
    )

st.sidebar.markdown("---")


if section == "SQL Projects":
    insurance_sql.show()

elif page == "Home":
    st.sidebar.caption("Contacts: german.rmnk@gmail.com")

    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">

        <h2>About me</h2>

        <p>
        My name is German Romanenko, and I am a data analyst passionate about transforming data into actionable business insights.
        </p>

        <p>
        This portfolio showcases projects covering data analysis, SQL, and dashboarding tools such as Power BI. 
        The objective is to demonstrate both technical skills and the ability to interpret data from a business perspective.
        </p>

        <p>
        I am particularly interested in roles where I can combine analytical thinking, problem-solving, and business understanding 
        to support data-driven decision-making.
        </p>

        

        <h2>How I Work with Data</h2>

        <p>
        I approach data analysis with a strong focus on business context.
        Each project is designed to answer concrete business questions and identify the key factors that drive performance.
        </p>
        
        <p>
        Beyond descriptive analysis, I aim to understand how different variables interact and how they impact outcomes such as revenue, customer behavior, or risk.
        </p>

        <p>
        In a real-world setting, I would adapt my approach to the specific needs of the business, incorporating additional data sources and using advanced methods (such as regression models) to quantify the impact of key drivers and support decision-making.
        </p>

        <p>
        My goal is always to translate data into clear, actionable insights that can support strategy and business growth.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif page == "Overview":
    st.title("E-commerce Data Analysis")
    st.markdown("---")
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")

    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818; border-left: 6px solid #7a1f1f; padding-left: 20px;">

     <h2 style="margin-top: 0; color: #442818;">Context</h2>

     <p>
     This project analyzes customer purchasing behavior in an e-commerce environment to identify key revenue drivers 
     and highlight actionable insights that can support data-driven business decisions.
     </p>

     <p>
     In a professional context, these analyses would rely on real internal customer data. 
     For confidentiality reasons, this project uses a synthetic dataset, allowing the demonstration of a structured analytical approach 
     and the type of insights typically derived in a business environment.
     </p>

        </div>
     """,
     unsafe_allow_html=True
    )

    st.markdown(
     """
     <div style="font-size: 30px; line-height: 1.8; color: #442818;">

     <h2 style="margin-top: 0; color: #442818;">Objectives</h2>

      <ul>
        <li>Analyze the distribution of order value to understand revenue structure</li>
        <li>Assess the impact of discounts on purchasing behavior</li>
        <li>Examine the relationship between pricing and quantities purchased</li>
        <li>Identify high-value customer segments and their contribution to revenue</li>
        <li>Evaluate product category performance and value drivers</li>
        <li>Understand how user behavior influences spending patterns</li>
      </ul>

     <p>
     This dataset contains transactional data used to illustrate customer behavior and revenue dynamics in an e-commerce context.
     </p>

      </div>
      """,
        unsafe_allow_html=True
    )

    st.header(" Dataset Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Orders", f"{len(df):,}")
    c2.metric("Customers", f"{df['Customer_ID'].nunique():,}")
    c3.metric("Average Order Value", f"{df['Total_Amount'].mean():,.0f}")
    c4.metric("Median Order Value", f"{df['Total_Amount'].median():,.0f}")
    st.dataframe(df.head(10), use_container_width=True)

elif page == "Average Order Value":
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")
    section_title("Distribution of Average Order Value")
    note(
        """
        In a real-world context, this type of analysis would help identify high-value customer segments and understand the contribution of large transactions to overall revenue. 
        It could support the design of targeted strategies, such as premium customer programs, personalized offers, or optimized pricing approaches aimed at maximizing revenue.
        """
    )

    total_orders = len(df)
    above_1000 = int((df["Total_Amount"] > 1000).sum())
    below_500 = int((df["Total_Amount"] <= 500).sum())
    pct_above_1000 = above_1000 / total_orders * 100
    pct_below_500 = below_500 / total_orders * 100
    top_10_cutoff = df["Total_Amount"].quantile(0.90)
    top_10_share = df.loc[df["Total_Amount"] >= top_10_cutoff, "Total_Amount"].sum() / df["Total_Amount"].sum() * 100

    fig, ax1 = make_fig()
    ax1.hist(df["Total_Amount"], bins=12, color=COLORS["primary"], edgecolor="white")
    ax1.set_title("Distribution of Average Order Value", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Order Amount")
    ax1.set_ylabel("Number of Orders")
    ax1.set_xlim(left=0)

    ax2 = ax1.twinx()
    ax2.set_facecolor(COLORS["bg"])
    ax2.tick_params(colors=COLORS["dark"])
    for spine in ax2.spines.values():
        spine.set_color(COLORS["soft"])
    df["Total_Amount"].plot(kind="kde", ax=ax2, color=COLORS["secondary"], linewidth=3)
    ax2.set_ylabel("")
    ax2.set_yticks([])
    ax2.spines["right"].set_visible(False)

    show_fig(fig)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Orders > 1,000", f"{above_1000:,}", f"{pct_above_1000:.1f}%")
    c2.metric("Orders <= 500", f"{below_500:,}", f"{pct_below_500:.1f}%")
    c3.metric("Mean", f"{df['Total_Amount'].mean():,.0f}")
    c4.metric("Median", f"{df['Total_Amount'].median():,.0f}")

    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">

      <p>
     Order values are strongly right-skewed: most transactions remain relatively small, while a limited number of high-value baskets significantly increase the overall average.
        This is also reflected in the gap between the mean and the median, which indicates the presence of large outlier transactions.
     </p>

     <p>
     This suggests that average order value should be interpreted with caution, as it is influenced by a relatively small share of very large purchases.
     Looking only at the average could therefore overestimate the typical customer basket.
      </p>

     <p>
      In a real-world context, this type of analysis would help identify the importance of high-value transactions in total revenue and support more targeted strategies,
      such as premium customer programs, personalized offers, or pricing approaches adapted to different basket profiles.
      </p>

      </div>
     """,
      unsafe_allow_html=True
    )

    cols_to_show = ["Order_ID", "Customer_ID", "Product_Category", "Unit_Price", "Quantity", "Discount_Amount", "Total_Amount"]
    st.subheader("Largest orders")
    st.dataframe(df.sort_values("Total_Amount", ascending=False)[cols_to_show].head(10), use_container_width=True)

elif page == "Discounts":
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")
    section_title("Discount Structure by Purchased Quantity")

    palette = ["#711D1B", "#BC9558", "#442818", "#9B592A", "#F6E0A0", "#C9A66B"]
    quantities = sorted(df["Quantity"].dropna().unique())
    order = ["0%", "5%", "10%", "15%", "20%", "25%"]

    fig, axes = plt.subplots(1, len(quantities), figsize=(3.8 * len(quantities), 4.2))
    fig.patch.set_facecolor(COLORS["bg"])

    if len(quantities) == 1:
        axes = [axes]

    for ax, q in zip(axes, quantities):
        ax.set_facecolor(COLORS["bg"])
        counts = df.loc[df["Quantity"] == q, "Discount_Label"].value_counts().reindex(order, fill_value=0)
        counts_nonzero = counts[counts > 0]
        colors_nonzero = palette[:len(counts_nonzero)]
        ax.pie(
            counts_nonzero,
            labels=counts_nonzero.index,
            autopct=lambda p: f"{p:.1f}%",
            startangle=90,
            colors=colors_nonzero,
            wedgeprops={"edgecolor": "white", "linewidth": 2},
            textprops={"color": COLORS["dark"], "fontsize": 9},
        )
        ax.set_title(f"Quantity = {int(q)}", fontweight="bold", color=COLORS["dark"])

    plt.suptitle("Discount Breakdown by Purchased Quantity", fontsize=18, fontweight="bold", color=COLORS["dark"])
    show_fig(fig)
    st.markdown("### New vs Returning Customers by Discount Level")

    df_analysis = df.copy()

    def label_discount(x):
        if x == 0:
            return "0%"
        elif 0 < x < 0.10:
            return "5-10%"
        elif 0.10 <= x < 0.15:
            return "10-15%"
        elif 0.15 <= x < 0.20:
            return "15-20%"
        else:
            return "20-22%"

    df_analysis["Discount_Label"] = df_analysis["Discount_Rate"].apply(label_discount)

    table = pd.crosstab(
        df_analysis["Discount_Label"],
        df_analysis["Is_Returning_Customer"],
        normalize="index"
    ) * 100

    order = ["0%", "5-10%", "10-15%", "15-20%", "20-22%"]
    table = table.reindex(order)

    table = table.rename(columns={False: "New Customers", True: "Returning Customers"})

    fig2, ax2 = make_fig((7.8, 4.8))

    table.plot(
        kind="bar",
        stacked=True,
        color=[COLORS["primary"], COLORS["secondary"]],
        ax=ax2,
        width=0.65
    )

    for container in ax2.containers:
        labels_bar = []
        for bar in container:
            h = bar.get_height()
            labels_bar.append(f"{h:.1f}%" if h >= 4 else "")
        ax2.bar_label(container, labels=labels_bar, label_type="center", color="white", fontsize=9)

    ax2.set_title("Share of New vs Returning Customers by Discount Level", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Discount rate")
    ax2.set_ylabel("Percentage")
    ax2.grid(axis="y", color=COLORS["accent"], alpha=0.2)
    ax2.legend(title="Customer type")
    plt.xticks(rotation=0)
    ax2.set_ylim(0, 100)

    show_fig(fig2)
    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">

     <p>
     Discount levels remain broadly similar across quantities purchased, suggesting that promotional policies are relatively uniform and not strongly tied to order size. 
     This indicates that discounts are not specifically used to encourage customers to increase their basket size, but are instead applied consistently regardless of purchase volume.
     </p>

      <p>
     In parallel, the share of new and returning customers remains stable across discount levels. 
      This suggests that promotions are not designed as a targeted acquisition strategy, but rather applied uniformly across the customer base without differentiating between new and existing customers.
      </p>

      <p>
       In a real-world context, these insights would support two distinct strategic questions: whether discounts can be used to increase basket size, 
     and whether they can effectively attract new customers. This type of analysis would help design more targeted promotional strategies, 
      aligning discount policies with specific business objectives such as customer acquisition or purchase uplift.
     </p>

     </div>
     """,
      unsafe_allow_html=True
    )

elif page == "Customer Value":
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")
    section_title("Customer Value Concentration")

    customer_spend = df.groupby("Customer_ID")["Total_Amount"].sum().sort_values(ascending=False)
    n_top = max(1, int(len(customer_spend) * 0.10))
    top_10_share = customer_spend.head(n_top).sum() / customer_spend.sum() * 100

    fig, ax = make_fig()
    x = range(1, len(customer_spend) + 1)
    cumulative_share = customer_spend.cumsum() / customer_spend.sum() * 100
    ax.plot(x, cumulative_share, color=COLORS["primary"], linewidth=2.5)
    ax.axvline(n_top, color=COLORS["accent"], linestyle="--", linewidth=2)
    ax.axhline(top_10_share, color=COLORS["secondary"], linestyle=":", linewidth=2)
    ax.set_title("Cumulative Revenue by Customer Rank", fontsize=18, fontweight="bold")
    ax.set_xlabel("Customer rank")
    ax.set_ylabel("Cumulative revenue share (%)")
    ax.set_ylim(0, 100)
    show_fig(fig)

    c1, c2 = st.columns(2)
    c1.metric("Top 10% customers", f"{n_top:,}")
    c2.metric("Revenue share", f"{top_10_share:.1f}%")

    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">

        <p>
        Customer value is unevenly distributed, with a subset of customers contributing more significantly to total revenue. 
        In this dataset, the top 10% of customers account for approximately 38.8% of total revenue.
        </p>

        <p>
        This reflects a moderate level of revenue concentration: while high-value customers play an important role, 
        the business is not overly dependent on a very small group of individuals. Revenue is still distributed across a broader customer base.
        </p>

        <p>
        In a real-world context, this type of analysis would support customer segmentation strategies. 
        High-value customers could be targeted with retention and loyalty initiatives, while the remaining customer base could be activated 
        through engagement and conversion strategies aimed at increasing their lifetime value.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

elif page == "Categories":
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")
    section_title("Product Category Performance")

    ca_cat = df.groupby("Product_Category")["Total_Amount"].sum().sort_values()
    avg_cat = df.groupby("Product_Category")["Total_Amount"].mean().sort_values()
    count_cat = df["Product_Category"].value_counts().sort_values()

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = make_fig()
        ax1.barh(ca_cat.index, ca_cat.values, color=COLORS["primary"])
        ax1.set_title("Revenue by Category", fontsize=14, fontweight="bold")
        ax1.set_xlabel("Total Revenue")
        ax1.set_ylabel("Category")
        ax1.grid(axis="x", color=COLORS["accent"], alpha=0.18)
        ax1.xaxis.set_major_formatter(FuncFormatter(money_formatter))
        st.pyplot(fig1, use_container_width=False)

    with col2:
        fig2, ax2 = make_fig()
        ax2.barh(avg_cat.index, avg_cat.values, color=COLORS["secondary"])
        ax2.set_title("Average Order Value by Category", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Average Order Value")
        ax2.set_ylabel("Category")
        ax2.grid(axis="x", color=COLORS["accent"], alpha=0.18)
        ax2.xaxis.set_major_formatter(FuncFormatter(money_formatter))
        st.pyplot(fig2, use_container_width=False)

    col3, col4 = st.columns(2)

    with col3:
        fig3, ax3 = make_fig()
        ax3.barh(count_cat.index, count_cat.values, color=COLORS["accent"])
        ax3.set_title("Number of Orders by Category", fontsize=14, fontweight="bold")
        ax3.set_xlabel("Number of Orders")
        ax3.set_ylabel("Category")
        ax3.grid(axis="x", color=COLORS["accent"], alpha=0.18)
        st.pyplot(fig3, use_container_width=False)

    with col4:
        st.markdown(
            """
            <div style="font-size: 30px; line-height: 1.8; color: #442818;">

             <p>
              Revenue differences across product categories are mainly driven by variations in average order value rather than purchase volume.
              While the number of orders remains relatively consistent, some categories generate significantly higher revenue due to higher-priced items.
              </p>

             <p>
              This highlights the coexistence of distinct category roles: certain categories act as high-value drivers, while others contribute through stable transaction volume.
             </p>

             <p>
             In a real-world context, this analysis would support category strategy by identifying premium segments to prioritize for margin optimization,
             as well as volume-driven categories that can be leveraged to drive traffic and customer acquisition.
             </p>
              </div>
             """,
             unsafe_allow_html=True
        )

elif page == "User Behavior":
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")
    section_title("User Behavior and Spending")

    session_amount = df.groupby("Session_Group", observed=False)["Total_Amount"].mean().reset_index()
    pages_amount = df.groupby("Pages_Group", observed=False)["Total_Amount"].mean().reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = make_fig((8, 5.2))
        ax1.plot(session_amount["Session_Group"].astype(str), session_amount["Total_Amount"], marker="o", color=COLORS["secondary"], linewidth=2.5)
        for i, val in enumerate(session_amount["Total_Amount"]):
            ax1.text(i, val + 20, f"{val:.0f}", ha="center", color=COLORS["dark"])
        ax1.set_title("Average Order Value by Session Duration", fontsize=18, fontweight="bold")
        ax1.set_xlabel("Session duration (minutes)")
        ax1.set_ylabel("Average order value")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = make_fig((8, 5.2))
        ax2.plot(pages_amount["Pages_Group"].astype(str), pages_amount["Total_Amount"], marker="o", color=COLORS["primary"], linewidth=2.5)
        for i, val in enumerate(pages_amount["Total_Amount"]):
            ax2.text(i, val + 20, f"{val:.0f}", ha="center", color=COLORS["dark"])
        ax2.set_title("Average Order Value by Pages Viewed", fontsize=18, fontweight="bold")
        ax2.set_xlabel("Pages viewed")
        ax2.set_ylabel("Average order value")
        st.pyplot(fig2)

    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">

         <p>
         User engagement shows different patterns depending on how it is measured. Session duration alone does not display a clear linear relationship with spending. 
         Short sessions are often associated with quick purchases and higher average order values, while mid-length sessions may reflect comparison behavior, leading to lower baskets. 
          Interestingly, very long sessions are again linked to higher order values, suggesting more deliberate and high-consideration purchases.
          </p>

         <p>
         In contrast, the number of pages viewed shows a strong and consistent positive relationship with average order value. 
         Customers who explore more pages tend to spend significantly more, indicating that browsing depth is a stronger signal of purchase intent than time spent.
          </p>

          <p>
         In a real-world context, this insight would support UX and conversion optimization strategies. Encouraging deeper product exploration 
         through recommendations, internal linking, or personalized journeys could be more effective than simply increasing session duration, 
         ultimately helping to increase basket size.
         </p>

         </div>
         """,
         unsafe_allow_html=True
    )

elif page == "Age & Categories":
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")
    section_title("Average Quantity by Age Group and Product Category")

    age_cat = df.groupby(["Age_Group", "Product_Category"], observed=False)["Quantity"].mean().reset_index()

    def lighten_color(color, amount=0.35):
        import matplotlib.colors as mcolors
        c = mcolors.to_rgb(color)
        return tuple(1 - (1 - x) * (1 - amount) for x in c)

    base_colors = [COLORS["primary"], COLORS["secondary"], COLORS["dark"], COLORS["accent"]]
    extended_palette = []
    for c in base_colors:
        extended_palette.append(c)
        extended_palette.append(lighten_color(c, 0.30))

    categories = list(df["Product_Category"].dropna().unique())

    fig, ax = make_fig((12, 6))
    for i, cat in enumerate(categories):
        data = age_cat[age_cat["Product_Category"] == cat]
        ax.plot(
            data["Age_Group"].astype(str),
            data["Quantity"],
            marker="o",
            label=cat,
            color=extended_palette[i % len(extended_palette)],
            linewidth=2,
            alpha=0.95,
        )
    ax.set_title("Average Quantity by Age Group and Category", fontsize=18, fontweight="bold")
    ax.set_xlabel("Age group")
    ax.set_ylabel("Average quantity")
    ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    show_fig(fig)

    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">

        <p>
        Purchased quantities remain relatively stable across age groups and product categories in this synthetic dataset, 
        which limits the identification of strong behavioral differences.
        </p>

        <p>
        In a real-world context, this type of analysis could reveal meaningful variations in purchasing behavior across age segments. 
        Identifying which age groups are more responsive to certain product categories or tend to purchase higher quantities would 
        enable more precise audience segmentation.
        </p>

        <p>
        These insights could directly support targeted advertising strategies, allowing businesses to tailor campaigns, messaging, 
        and promotions to specific age groups, ultimately improving engagement and marketing efficiency.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

elif page == "Geography":
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")
    section_title("Geographic Revenue Distribution")

    top_n = 7
    city_ca = df.groupby("City")["Total_Amount"].sum()
    top_cities = city_ca.sort_values(ascending=False).head(top_n)
    others = city_ca.sum() - top_cities.sum()
    top_cities["Others"] = others
    top_cities = top_cities.sort_values()

    fig, ax = make_fig((10, 5.8))
    ax.barh(top_cities.index, top_cities.values, color=COLORS["primary"])
    ax.set_title("Revenue by City (Top + Others)", fontsize=18, fontweight="bold")
    ax.set_xlabel("Total revenue")
    ax.set_ylabel("City")
    ax.grid(axis="x", color=COLORS["accent"], alpha=0.18)
    ax.xaxis.set_major_formatter(FuncFormatter(money_formatter))
    show_fig(fig)

    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">

        <p>
        Purchased quantities remain relatively stable across age groups and product categories in this synthetic dataset, 
        which limits the identification of strong behavioral differences.
        </p>

        <p>
        In a real-world context, this type of analysis could reveal meaningful variations in purchasing behavior across age segments. 
        Identifying which age groups are more responsive to certain product categories or tend to purchase higher quantities would 
        enable more precise audience segmentation.
        </p>

        <p>
        These insights could directly support targeted advertising strategies, allowing businesses to tailor campaigns, messaging, 
        and promotions to specific age groups, ultimately improving engagement and marketing efficiency.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

elif page == "Delivery & Satisfaction":
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")
    section_title("Customer Satisfaction vs Delivery Time")

    rating_delivery = df.groupby("Delivery_Group", observed=False)["Customer_Rating"].mean().reset_index()

    fig, ax = make_fig((8, 5.2))
    bars = ax.bar(rating_delivery["Delivery_Group"].astype(str), rating_delivery["Customer_Rating"], color=COLORS["primary"], width=0.6)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.02, f"{h:.2f}", ha="center", color=COLORS["dark"], fontweight="bold")

    ax.set_title("Average Customer Rating by Delivery Time", fontsize=18, fontweight="bold")
    ax.set_xlabel("Delivery time")
    ax.set_ylabel("Average rating")
    show_fig(fig)

    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">

         <p>
          In this synthetic dataset, customer satisfaction remains relatively stable across delivery time ranges, suggesting no strong observable relationship.
          </p>

          <p>
          In a real-world context, however, delivery time is typically a key driver of customer satisfaction. Faster deliveries are generally associated with higher satisfaction,
          while delays or variability in delivery performance can significantly impact the customer experience.
          </p>

          <p>
          Beyond average delivery time, consistency and reliability often play an even more critical role. Customers tend to tolerate longer delivery times if expectations are clearly communicated,
            but unexpected delays can lead to frustration and lower ratings.
          </p>

         <p>
          This type of analysis would therefore be essential to evaluate logistics performance, identify service bottlenecks, and optimize delivery strategies.
         It could support decisions such as improving last-mile operations, setting more accurate delivery promises, or prioritizing faster shipping options for high-value customers.
          </p>

          </div>
         """,
        unsafe_allow_html=True
    )

elif page == "Conclusion":
    st.sidebar.caption("Synthetic dataset used for demonstration purposes.")
    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">
        <h2 style="margin-top: 0; color: #442818;">Conclusion</h2>

        <p>
        This project demonstrates a structured analytical approach to understanding customer behavior in an e-commerce environment, 
        from exploratory analysis to the extraction of actionable business insights.
        </p>

        <h3 style="color: #442818;">Key takeaways</h3>

        <ul>
        <li>Revenue is concentrated among a relatively small group of high-value customers, highlighting the importance of customer segmentation.</li>
        <li>Product categories contribute differently to performance, with some acting as high-value drivers and others as volume generators.</li>
        <li>User engagement, particularly through pages viewed, appears to be a strong indicator of higher basket sizes.</li>
        <li>Some relationships remain limited due to the homogeneous nature of the synthetic dataset.</li>
        </ul>

        <p>
        While the dataset limits the ability to uncover strong statistical relationships, the analysis reflects a realistic business framework. 
        In a real-world context, richer and more variable data would allow for deeper modeling of purchase drivers and more precise optimization strategies.
        </p>

        <h3 style="color: #442818;">Final note</h3>

        <p>
        The objective of this portfolio project is to demonstrate the ability to structure an end-to-end analysis, 
        translate data into business-oriented insights, and present results in a clear and professional way.
        </p>

        <p>
        Even when working with synthetic data, the methodology remains fully transferable to real-world business problems.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
elif page == "Next Step With Real Data":
    st.markdown(
        """
        <div style="font-size: 30px; line-height: 1.8; color: #442818;">
        <h2 style="margin-top: 0; color: #442818;">Next Step</h2>

        <p>
        This project is based on a synthetic dataset, which limits the depth of statistical relationships.
        With real-world data, several advanced analyses could be developed to go further and support business decisions.
        </p>

        <h3 style="color: #442818;">1. Customer Segmentation</h3>

        <p>
       Using behavioral and transactional data to identify high-value segments (e.g., RFM analysis) and tailor marketing strategies.
        </p>

        <h3 style="color: #442818;">2. Pricing & Discount Optimization</h3>

        <p>
       Applying regression models to measure the impact of pricing and discounts on revenue and demand, enabling more effective promotional strategies.
        </p>

        <h3 style="color: #442818;">3. Customer Lifetime Value (CLV)</h3>

        <p>
       Estimating long-term customer value to prioritize retention efforts and optimize acquisition costs.
        </p>

        <h3 style="color: #442818;">4. Predictive Modeling</h3>

        <p>
       Building models to predict purchasing behavior, basket size, or churn probability.
        </p>

        <h3 style="color: #442818;">5. Personalization & Recommendation</h3>

        <p>
       Leveraging browsing behavior (pages viewed, session data) to improve product recommendations and increase conversion rates
        </p>

        <p>
       These approaches would allow the transition from descriptive insights to predictive and prescriptive analytics, supporting more strategic and data-driven decision-making.
        </p>

        <p>
       If you'd like to explore how these types of analyses could be applied to your business, feel free to get in touch.
        </p>
        

        </div>
        """,
        unsafe_allow_html=True
    )

elif page == "Dashboard Overview":
    st.title("Power BI")
    st.info("Power BI section coming soon.")

elif page == "Key Metrics":
    st.title("Power BI")
    st.info("Power BI section coming soon.")

elif page == "Insights":
    st.title("Power BI")
    st.info("Power BI section coming soon.")