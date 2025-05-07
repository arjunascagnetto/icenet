from icenet.model.train import train_model

trained_path, history = train_model(
    run_name="api_test_run",
    dataset=dataset,
    epochs=10,
    n_filters_factor=0.6,
    seed=42,
    strategy=strategy,
    training_verbosity=2,
)
