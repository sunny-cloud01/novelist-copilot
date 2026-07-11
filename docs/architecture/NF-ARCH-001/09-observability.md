# 9. Observability Requirements

Novel Factory must record operational and knowledge-engineering signals.

Required signal groups:

- ingestion_metrics
- extraction_metrics
- validation_metrics
- generation_metrics
- consistency_metrics
- review_metrics
- feedback_metrics

Each pipeline run must produce a traceable run_id.

Minimum trace fields:

- run_id
- module_name
- input_ids
- output_ids
- status
- started_at
- finished_at
- error_id
