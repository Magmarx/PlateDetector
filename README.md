# Python Plate Detector For Openalpr

This project implements the openalpr library for detecting plates, for generating reports and analyse multiple types of results from the plates.

## Getting Started

These instructions will give you a guideline of how you can use the library and basically how it spects the input values.

### Prerequisites

For you to run this commands you will have to install 5 other things:

* [openalpr](https://github.com/openalpr/openalpr) - The library that we will use to detect the plates
* [Python 3.6](https://www.python.org/downloads/) - This is the python version we are currently using
* [Arrow](https://arrow.readthedocs.io/en/latest/) - Used for dates and times
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/) - Used for creating the excel reports


### Command lines and options

We have multiple options for running the report generator for example 

```
python main.py --file filepath --opcion --noDel jsonData --report date time
```

* --file/--folder the type of read you want to execute
* filepath the place where we have our tests
* --opcion we have multiple options for this one
    * --text create's a .txt file with the report data    
    * --log this will print the log on the terminal
* --noDel/--del delete video flag
* jsonData send ''
* --report this flag will tell the program to sort the videos by code, date, schedule

For generating the plate report use:

```
python reportGenerator.py --folder --reportType  --dev/prod path
```

* --folder the folder with the sorted results
* --reportType can be (--Early_Morning/--Morning/--Afternoon/--Night)
* --dev/prod will generate diferent types of reports
    * --dev will generate a report with the cars and not cars with the result report
    * --prod will only generate the result report
* path the place where we have our tests

## Help with the openpyxl library

when you want to use the file images like png, jpeg, bmp install the dependence -- pip install pillow
* [openpyxl documentation](https://openpyxl.readthedocs.io/en/stable/)
* [openpyxl tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html#create-a-workbook)

## Authors

* **Miguel Angel Porras** - *Initial work* - [Magmarx](https://github.com/Magmarx)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details