import pathlib

import yaml

import UserInterface


def load_user_input(file_path):

    # TODO check file_path for errors/non-existent files and so on

    file_path = pathlib.Path(file_path)

    with open(str(file_path), "r") as file_descriptor:
        # The "FullLoader" is not mentioned in the documentation but there is a
        # wiki page about it on the package's github:
        # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load%28input%29-Deprecation
        yaml_content = yaml.load(file_descriptor, Loader=yaml.FullLoader)

    yaml_box_extent = yaml_content['Pile extent']
    yaml_box_extent['Width']
    yaml_box_extent['Height']
    yaml_box_extent['Depth']

    yaml_rand_stem = yaml_content['Random stem generation']
    random_stem_user_input = UserInterface.Input.RandomStemGeneration(
        num_stems=yaml_rand_stem['Number of stems'],
        length_mean=yaml_rand_stem['Length']['mean'],
        length_sd=yaml_rand_stem['Length']['standard deviation'],
        middle_stem_diameter_mean=yaml_rand_stem['Middle stem diameter']['mean'],
        middle_stem_diameter_sd=yaml_rand_stem['Middle stem diameter']['standard deviation'],
        ellipticity_sd=yaml_rand_stem['Ellipticity standard deviation'],
        stem_taper_mean=yaml_rand_stem['Stem taper']['mean'],
        stem_taper_sd=yaml_rand_stem['Stem taper']['standard deviation'],
        bend_mean=yaml_rand_stem['Mean bend']
    )

    return UserInterface.Input(random_stem_generation=random_stem_user_input)


def yaml_loader(file_path):
    with open(file_path, "r") as file_descriptor:
        # The "FullLoader" is not mentioned in the documentation but there is a
        # wiki page about it on the package's github:
        # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load%28input%29-Deprecation
        return yaml.load(file_descriptor, Loader=yaml.FullLoader)


def yaml_dump(file_path, data):
    with open(file_path, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)


if __name__ == "__main__":
    user_settings_file_path = "simulation_settings.yaml"
    user_settings = yaml_loader(user_settings_file_path)
    print(user_settings)

    stem_settings = user_settings.get('Random stem generation')
    for stem_settings_name, stem_settings_value in stem_settings.items():
        print(stem_settings_name, stem_settings_value)
