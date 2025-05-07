from icenet.data.dataset import IceNetDataSet
from icenet.model.models import unet_batchnorm
import tensorflow as tf

start_dates = [el.date() for el in pd.date_range("2020-04-01", "2020-04-02")]

# initialise IceNetDataSet and obtain data loader used to generate the dataset config
ds = IceNetDataSet(dataset_config, batch_size=4)
dl = ds.get_data_loader()

logging.info("Generating forecast inputs from processed/ files")

# generate samples for prediction
forecast_inputs, gen_outputs, sample_weights = \
    list(zip(*[dl.generate_sample(date, prediction=True) for date in start_dates]))

network_folder = os.path.join(".", "results", "networks", "custom_run")

dataset_name = ds.identifier
network_path = os.path.join(network_folder,
                            "{}.network_{}.{}.h5".format(run_name,
                                                         "api_dataset",
                                                         seed))

logging.info("Loading model from {}...".format(network_path))

network = unet_batchnorm(
    (*ds.shape, dl.num_channels),
    [],
    [],
    n_filters_factor=0.6,
    n_forecast_days=ds.n_forecast_days
)
network.load_weights(network_path)

predictions = []

for i, net_input in enumerate(forecast_inputs):
    logging.info("Running prediction {} - {}".format(i, start_dates[i]))
    pred = network(tf.convert_to_tensor([net_input]), training=False)
    predictions.append(pred)
