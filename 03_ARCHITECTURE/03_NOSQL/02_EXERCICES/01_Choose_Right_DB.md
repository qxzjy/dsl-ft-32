# Choose the right DB 🍒

## Context 1
An online trading company needs to store critical transactional data such as stock trades, with high consistency and availability. Cost is an important factor as the company needs to store large amounts of data over a long period for analysis. Stock trades require high consistency to ensure data integrity, and high availability to prevent service interruptions. However, the company must also consider costs, as trades are recorded in real time and generate a large amount of data.

Consistency: High\
Availability: High\
Cost: Important\
💡 Recommended Database Type: **Relational database**

Explanation: A relational database offers high consistency and availability for transactional data. Additionally, a relational database can handle large amounts of data and allows advanced data analysis, which is important for a trading company. However, a relational database can be expensive to scale, so the company must consider cost.

## Context 2
A social media company needs to store unstructured data such as images, videos, and messages with high availability and partition tolerance. Consistency is less critical as there are no major consequences if the data is not perfectly consistent. Cost must be managed efficiently, as the company is in the startup phase and has a limited budget.

Consistency: Low\
Availability: High\
Cost: Medium\
💡 Recommended Database Type: **Document-oriented database**

Explanation: A document-oriented database can store unstructured data flexibly with high availability and partition tolerance. Consistency is less critical in this case as unstructured data can be stored and displayed flexibly. Cost must be managed efficiently, as the company has a limited budget.

## Context 3
An e-commerce company needs to store product catalog data with high consistency and availability. Cost is not a critical factor as the company has a significant budget for data infrastructure.

Consistency: High\
Availability: High\
Cost: Not Critical\
💡 Recommended Database Type: **Relational database**

Explanation: A relational database offers high consistency and availability for product catalog data. The company has a significant budget for data infrastructure, so the cost is not a critical factor.

## Context 4
An energy management company needs to store measurement data with high availability and partition tolerance. Consistency is not critical and cost must be minimised.

Consistency: Low\
Availability: High\
Cost: Low\
💡 Recommended Database Type: **Column-oriented database**

Explanation: A column-oriented database can store measurement data efficiently with high availability and partition tolerance. Consistency is not critical in this case, and cost must be minimised, so a column-oriented database is a good choice.

## Context 5
A travel company needs to store location data with low consistency but high availability. Cost must be minimised.

Consistency: Low\
Availability: High\
Cost: Low\
💡 Recommended Database Type: **Key-value database**

Explanation: A key-value database can store location data efficiently with high availability and partition tolerance. Consistency is low in this case, and cost must be minimised, so a key-value database is a good choice.