from setuptools import setup, find_packages


setup(
    name="MusicPet",
    version="0.1",
    packages=find_packages(exclude=["tests", "scripts"]),
    entry_points={
        "console_scripts": [
            "metaallmusic = scripts.metaallmusic:print_dir_meta"
        ]
    },
    author="Gates_ice",
    author_email="gates@gatesice.com",
    description="A pet that manage all your music",
    keywords="music lossless flac cue"
)

