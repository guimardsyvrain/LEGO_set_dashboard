# LEGO Set Explorer Dashboard

## Overview
LEGO enthusiasts and collectors often face challenges when searching through thousands of LEGO sets distributed across multiple datasets, themes, and release periods. Filtering sets based on specific preferences such as theme, age range, piece count, or product category can become time-consuming and inefficient when data is fragmented and difficult to explore.

This solution was designed to centralize and transform LEGO product data into an interactive analytics experience using Power BI and a modern end-to-end data pipeline. The dashboard enables users to efficiently explore LEGO sets using dynamic search and filtering capabilities based on set name, theme, subtheme, age category, piece count, pricing, and product availability.

Interactive visualizations and drill-through features provide deeper insights into LEGO collections and product characteristics, while embedded URLs allow users to quickly access additional information for each set.
By transforming raw LEGO datasets into a user-friendly exploration platform, the solution improves product discovery, simplifies decision-making for collectors, and demonstrates how business intelligence tools can enhance customer experience through interactive data visualization and scalable analytics.

## Solution Architecture
The solution was designed to transform fragmented LEGO datasets into a scalable and interactive analytics platform that improves product exploration and user experience.
The architecture was developed through the following stages:
1.	Defining the key search and analysis dimensions driving LEGO set exploration, including set ID, category, theme, subtheme, age range, piece count, and pricing. 
2.	Building an automated data ingestion pipeline in Microsoft Fabric to centralize raw LEGO datasets into a Bronze layer. 
3.	Processing and transforming the raw data using Python notebooks to clean, enrich, and structure analytics-ready datasets for reporting and visualization. 
4.	Developing an interactive Power BI dashboard composed of three analytical views: 
   * A high-level overview of LEGO sets by category, age range, pricing, and yearly trends. 
   * An intelligent search and filtering interface providing detailed set-level insights through dynamic exploration capabilities. 
   * A decomposition tree analysis enabling users to drill down into LEGO collections by theme, subtheme, category, and set name for deeper product analysis.
     
This architecture demonstrates how modern data engineering and business intelligence solutions can transform large-scale product datasets into an intuitive and data-driven exploration experience. Click on the link below to access the dashboard:
https://app.fabric.microsoft.com/groups/d41978dc-b7f2-446f-a482-c56bfa049e3d/reports/25b9315f-7538-4827-a555-ee9ed091ade6/0ff078c61f0aa5fe6719?experience=fabric-developer
