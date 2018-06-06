import setuptools

setuptools.setup(
    name="django-format-sql",
    version="0.0.1",
    author="Robin Ramael",
    author_email="robin.ramael@gmail.com",
    description=("Print formatted sql queries when "
                 "TestCase.assertNumQueries fails."),
    url="https://github.com/RobinRamael/django-format-sql",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'Django>1.2'
    ]
)
