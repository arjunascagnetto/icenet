from icenet.data.dataset import IceNetDataSet
from icenet.model.models import unet_batchnorm
import icenet.model.losses as losses
import icenet.model.metrics as metrics

# train_model sets up wandb and attempts seeding here (see icenet#8 for issues around multi-GPU determinism)
seed = 45
os.environ['PYTHONHASHSEED'] = str(seed)
np.random.seed(seed)
random.seed(seed)
tf.random.set_seed(seed)
tf.keras.utils.set_random_seed(seed)

# initialise IceNetDataSet
ds = IceNetDataSet(dataset_config, batch_size=4)

input_shape = (*ds.shape, ds.num_channels)
train_ds, val_ds, test_ds = ds.get_split_datasets()

# train_model handles pickup runs/trained networks
run_name = "custom_run"
network_folder = os.path.join(".", "results", "networks", run_name)

if not os.path.exists(network_folder):
    logging.info("Creating network folder: {}".format(network_folder))
    os.makedirs(network_folder)

network_path = os.path.join(network_folder,
                            "{}.network_{}.{}.h5".format(run_name,
                                                         ds.identifier,
                                                         seed))

callbacks_list = list()
# train_model sets up various callbacks: early stopping, lr scheduler, 
# checkpointing, wandb and tensorboard

with strategy.scope():
    loss = losses.WeightedMSE()
    metrics_list = [
        metrics.WeightedMAE(),
        metrics.WeightedRMSE(),
        losses.WeightedMSE()
    ]

    network = unet_batchnorm(
        input_shape=input_shape,
        loss=loss,
        metrics=metrics_list,
        learning_rate=1e-4,
        filter_size=3,
        n_filters_factor=0.6,
        n_forecast_days=ds.n_forecast_days,
    )

# train_model loads weights
network.summary()

model_history = network.fit(
    train_ds,
    epochs=5,
    verbose=2,
    callbacks=callbacks_list,
    validation_data=val_ds,
    max_queue_size=10,
)

logging.info("Saving network to: {}".format(network_path))
network.save_weights(network_path)
