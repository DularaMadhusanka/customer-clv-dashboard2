# Customer Value & Retention Dashboard

This Streamlit dashboard converts the two-stage CLV model output into business actions.

## Files

- `app.py` — dashboard application
- `customer_clv_dashboard.csv` — dashboard dataset
- `requirements.txt` — Python dependencies

## Run locally

1. Put `customer_clv_dashboard.csv` in the same folder as `app.py`.
2. Open a terminal in that folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

The terminal will display a local URL, usually `http://localhost:8501`.

## Dashboard pages

- **Business overview:** portfolio KPIs, CLV segments and the customer opportunity map.
- **Customer priorities:** ranked customer action list with CSV download.
- **Revenue planning:** campaign scenario calculator and market-level value.
- **How the score works:** non-technical explanation, model inputs and validation metrics.

## Important interpretation

`PredictedCLV` is an expected future-period revenue proxy:

`RepeatProbability × ConditionalFutureRevenue`

The campaign calculator is a scenario-planning tool. Its uplift input is an assumption, not a causal effect estimated by the model.
