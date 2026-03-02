import pandas as pd
from expectations import gx
from great_expectations.core.run_identifier import RunIdentifier
from config import datasource_name, asset_name, expectation_suite_name, validation_name, checkpoint_name, batch_definition_name
from utils import define_suite, define_valildation, define_checkpoint, define_batch_definition

df = pd.read_csv("data.csv")
context = gx.get_context(mode="file")
print(context)

existing_sources = list(context.data_sources.all().keys())
existing_suites = [st.name for st in context.suites.all()]
existing_validations = [vd.name for vd in context.validation_definitions.all()]
existing_checkpoints = [ch.name for ch in context.checkpoints.all()]
action_list = [
    gx.checkpoint.UpdateDataDocsAction(
        name="update_all_data_docs",
    ),
]

batch_definition = define_batch_definition(context, datasource_name, existing_sources, asset_name, batch_definition_name)
suite = define_suite(context, df, existing_suites, expectation_suite_name)
validation_definition = define_valildation(context, existing_validations, batch_definition, suite, validation_name)
validation_results = define_checkpoint(context, df, existing_checkpoints, validation_definition, action_list, checkpoint_name)

print(validation_results)

context.build_data_docs()
context.open_data_docs()

