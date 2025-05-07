from icenet.data.loaders import IceNetDataLoaderFactory
import logging


def main():
	implementation = "dask"
	loader_config = "loader.tutorial_api_data.json"
	dataset_name = "api_dataset"
	lag = 1

	dl = IceNetDataLoaderFactory().create_data_loader(
    implementation,
    loader_config,
    dataset_name,
    lag,
    n_forecast_days=7,
    north=True,
    south=False,
    output_batch_size=4,
    generate_workers=8)

	dl.generate()


if __name__ == "__main__":
    main()
