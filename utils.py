import pandas as pd
from expectations import gx, verify_all_distinct_values, verify_columns_number, verify_columns_values
from great_expectations.core.run_identifier import RunIdentifier
from datetime import datetime

def reading_source_df(field_name) :
    if field_name == "telecom_churn" :
        df = pd.read_csv("source_df.csv")
    return df

def define_batch_definition(context, datasource_name, existing_sources, asset_name, batch_definition_name) :
    
    if datasource_name in existing_sources: 
        data_source = context.data_sources.get(datasource_name)  
        data_asset = data_source.get_asset(asset_name) 
        batch_definition = data_asset.get_batch_definition(batch_definition_name)
        print("Datasource existant récupéré")

    else:
        data_source = context.data_sources.add_pandas(datasource_name)
        data_asset = data_source.add_dataframe_asset(asset_name) 
        batch_definition = data_asset.add_batch_definition_whole_dataframe(batch_definition_name)
        print("Datasource créée.")

    return batch_definition


def define_suite(context, source_df, existing_suites, expectation_suite_name) :

    if expectation_suite_name in existing_suites :
        suite = context.suites.get(name=expectation_suite_name)
    else :
        suite = context.suites.add(gx.ExpectationSuite(name=expectation_suite_name))
        data_expectations = [verify_all_distinct_values(source_df, "churn"), verify_columns_number(source_df), verify_columns_values(source_df)]
        for ex in data_expectations :
            suite.add_expectation(ex)

    return suite


def define_valildation(context, existing_validations, batch_definition, suite, validation_name) :
    
    if validation_name in existing_validations : 
        validation_definition = context.validation_definitions.get(name=validation_name)
    else :
        validation_definition = gx.ValidationDefinition(
            data=batch_definition, suite=suite, name=validation_name
        )
        validation_definition = context.validation_definitions.add(validation_definition)

    return validation_definition


def define_checkpoint(context, df, existing_checkpoints, validation_definition, action_list, checkpoint_name) :

    custom_run_id = RunIdentifier(
        run_name="Hans Ariel", 
        run_time=datetime.now()
    )

    if checkpoint_name in existing_checkpoints : 
        checkpoint = context.checkpoints.get(name=checkpoint_name)
    else :
        checkpoint = gx.Checkpoint(
            name=checkpoint_name,
            validation_definitions=[validation_definition],
            actions=action_list,
            result_format={"result_format": "COMPLETE"},
        )
        context.checkpoints.add(checkpoint)

    validation_results = checkpoint.run(
        batch_parameters={"dataframe": df},
        run_id=custom_run_id
    )

    return validation_results


