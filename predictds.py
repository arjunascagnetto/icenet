from icenet.model.predict import predict_forecast

# Follows the naming convention used by the CLI version
output_dir = os.path.join(".", "results", "predict",
                          "custom_run_forecast",
                          "{}.{}".format(run_name, "42"))

predict_forecast(
    dataset_config=dataset_config,
    network_name=run_name,
    n_filters_factor=0.6,
    output_folder=output_dir,
    seed=seed,
    start_dates=[pd.to_datetime(el).date()
                 for el in pd.date_range("2020-04-01", "2020-04-02")],
    test_set=True,
)
