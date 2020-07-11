import pathlib
import os #testweise


import yaml

import UserInterface


def load_user_input(file_path): #-> List[UserInterface.Input]
    """Tries to create a user input object from the contents of a YAML file
    supplied by the user.

    Raises:
    -------
    + RuntimeError -- If no file could be found at the location of file_path.
    + ValueError -- If the file doesn't contain all expected keys.
    """

    file_path = pathlib.Path(file_path)

    if not file_path.exists():
        raise RuntimeError(
            'Could not find file with simulation settings at path:\n"{0}"'.format(
                file_path.as_posix()
            )
        )

    with open(str(file_path), "r") as file_descriptor:
        # The "FullLoader" is not mentioned in the documentation but there is a
        # wiki page about it on the package's github:
        # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load%28input%29-Deprecation
        yaml_content = yaml.load(file_descriptor, Loader=yaml.FullLoader)

    try:

        box_extent = yaml_content['Pile extent']
        random_stem_gen = yaml_content['Random stem generation']

        return [UserInterface.Input(
            UserInterface.Input.BoxExtent(
                width=box_extent['Width'],
                height=box_extent['Height'],
                depth=box_extent['Depth']
            ),
            UserInterface.Input.RandomStemGeneration(
                num_stems=random_stem_gen['Number of stems'],
                length_mean=random_stem_gen['Length']['mean'],
                length_sd=random_stem_gen['Length']['standard deviation'],
                middle_stem_diameter_mean=random_stem_gen
                ['Middle stem diameter']['mean'],
                middle_stem_diameter_sd=random_stem_gen
                ['Middle stem diameter']['standard deviation'],
                ellipticity_sd=random_stem_gen
                ['Ellipticity standard deviation'],
                stem_taper_mean=random_stem_gen['Stem taper']['mean'],
                stem_taper_sd=random_stem_gen
                ['Stem taper']['standard deviation'],
                bend_mean=random_stem_gen['Mean bend']
            ),
            iterations = yaml_content['Number of iterations'],
            stems_file_path = yaml_content['Load stems from file path']
        )]

    except KeyError as original_exc:
        raise ValueError(
            'Not all necessary keys present for user input creation!'
        ) from original_exc
