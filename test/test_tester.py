from fastNLP.core.tester import POSTester
from fastNLP.loader.config_loader import ConfigSection, ConfigLoader
from fastNLP.loader.dataset_loader import TokenizeDatasetLoader
from fastNLP.loader.preprocess import POSPreprocess
from fastNLP.models.sequence_modeling import SeqLabeling

data_name = "pku_training.utf8"
cws_data_path = "/home/zyfeng/Desktop/data/pku_training.utf8"
pickle_path = "data_for_tests"


def foo():
    loader = TokenizeDatasetLoader(data_name, cws_data_path)
    train_data = loader.load_pku()

    train_args = ConfigSection()
    ConfigLoader("config.cfg", "").load_config("./data_for_tests/config", {"POS": train_args})

    # Preprocessor
    p = POSPreprocess(train_data, pickle_path)
    train_args["vocab_size"] = p.vocab_size
    train_args["num_classes"] = p.num_classes

    model = SeqLabeling(train_args)

    valid_args = {"save_output": True, "validate_in_training": True, "save_dev_input": True,
                  "save_loss": True, "batch_size": 8, "pickle_path": "./data_for_tests/",
                  "use_cuda": True}
    validator = POSTester(valid_args)
    validator.test(model)
    validator.show_matrices()


if __name__ == "__main__":
    foo()
