/**********************************************************************
 Ibotta Analytics Engineering Take‑Home
**********************************************************************/

----------------------------------------------------------------------
-- Exploratory Review of Tables
----------------------------------------------------------------------

-- customer_offer_redemptions
-- Columns:
-- id, customer_offer_id, verified_redemption_count,
-- submitted_redemption_count, offer_amount, created_at

SELECT * FROM customer_offer_redemptions limit 100;

-- customer_offer_rewards
-- id, customer_id, offer_reward_id, finished, created_at

SELECT * FROM customer_offer_rewards limit 100;

-- customer_offers
-- id, customer_id, offer_id, activated, verified

SELECT * FROM customer_offers limit 100;

-- offer_rewards
-- id, offer_id, type, amount, created_at, updated_at

SELECT * FROM offer_rewards limit 100;


----------------------------------------------------------------------
-- Question 1:
-- What is the total count of offer activations for each customer?
----------------------------------------------------------------------

-- Validate uniqueness of customer_offers.id
-- If any rows return, the ID cannot be safely used as a unique key

SELECT
id,
COUNT(*) AS row_count
FROM customer_offers
GROUP BY id
HAVING COUNT(*) > 1;

-- Count activated offers per customer
SELECT
customer_id,
COUNT(DISTINCT id) AS offer_activations
FROM customer_offers
GROUP BY customer_id
ORDER BY offer_activations DESC;

----------------------------------------------------------------------
-- Question 2:
-- Which customers have not activated an offer in the last couple months?
----------------------------------------------------------------------

-- order the activated column by both asc/desc to get a feel for the data
SELECT *
FROM customer_offers
WHERE activated IS NOT NULL
ORDER BY activated;

-- See the date range within the activated column
SELECT
    MIN(activated) AS min_activated,
    MAX(activated) AS max_activated
FROM customer_offers;

-- Note:
-- The dataset only spans ~2021‑03‑18 to 2021‑03‑25.
-- Therefore “no recent activation” is interpreted as:
-- customers who have NEVER activated an offer (activated IS NULL).

SELECT
    customer_id,
    MAX(activated) AS last_activation
FROM customer_offers
GROUP BY customer_id
HAVING MAX(activated) IS NULL
ORDER BY last_activation;

-- Hypothetical solution if historical data existed, I would have used a max activated date two months before the max date in the table
SELECT
    customer_id,
    MAX(activated) AS last_activation
FROM customer_offers
GROUP BY customer_id
HAVING MAX(activated) < DATE('2021-01-25')
ORDER BY last_activation DESC;


----------------------------------------------------------------------
-- Question 3:
-- What is the conversion rate from activated to completed offers
-- for each customer?
----------------------------------------------------------------------


--Assuming that the conversion rate is the ratio of completed / activated offers
--adding in the numerator and denominator to get a sense of scale, and to use in further analytics
--ordering by the highest conversion rate, to see who is completing the most activated offers, but can order by the opposite to see who is often activating but not following through
--The ones not following through with activations could be used in a targeting campaign to try to boost conversions 
--conversion techniques could be better deals, less steps in the process (transaction record vs. uploading a picture of your receipt), etc. 
--A/B test with low conversion group

SELECT
customer_id,
COUNT(CASE WHEN verified IS NOT NULL THEN id END) AS completed_offers,
COUNT(CASE WHEN activated IS NOT NULL THEN id END) AS activated_offers,
ROUND(
    100.0 * COUNT(CASE WHEN verified IS NOT NULL THEN id END)
    / NULLIF(COUNT(CASE WHEN activated IS NOT NULL THEN id END), 0),
    2
) || '%' AS conversion_rate
FROM customer_offers
GROUP BY customer_id
ORDER BY ROUND(100.0 * COUNT(CASE WHEN verified IS NOT NULL THEN id END) / NULLIF(COUNT(CASE WHEN activated IS NOT NULL THEN id END), 0), 2) DESC,
completed_offers DESC,
activated_offers DESC;


----------------------------------------------------------------------
-- Question 4:
-- What is the total redemption amount for each customer?
----------------------------------------------------------------------

-- Validate join key uniqueness
-- no rows means unique

SELECT
customer_offer_id,
COUNT(*) AS row_count
FROM customer_offer_redemptions
GROUP BY customer_offer_id
HAVING COUNT(*) > 1;

-- Calculate redemption totals per offer activation
-- Explored both tables to find the column key
-- aware there is a 1 to many relationship, so ensuring I am not duplicating the results
-- added in total redemption amount to get a sense of total amount going back to the customers, size of the offer, etc. 

SELECT
c.customer_id,
c.id AS customer_offer_id,
SUM(o.verified_redemption_count) AS verified_redemption_count,
SUM(o.verified_redemption_count * o.offer_amount) AS total_redemption_amount
FROM customer_offers c
LEFT JOIN customer_offer_redemptions o
    ON c.id = o.customer_offer_id
GROUP BY
c.customer_id,
c.id
ORDER BY verified_redemption_count DESC;


----------------------------------------------------------------------
-- Spot validation for a single customer_offer_id
----------------------------------------------------------------------

SELECT *
FROM customer_offer_redemptions
WHERE customer_offer_id = 19956623672;

SELECT *
FROM customer_offers
WHERE id = 19956623672;