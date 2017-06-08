# Error Functions of robot movements and measurements

We will need functions describing the error we deal with in our measurements and movements for the particle filter. Therefore we use polynomial regression to fit a function in measured errors. This can be achieved by doing lots of tests, saving the data in csv-files and running a script on it.

## Csv file format

Save the measured data in an csv-file (**c**omma **s**eparated **v**alue). Is is called csv, because you will simply need to seperate each value with a comma. In the end, it should look like this:

|reality, | measurement |
|---- | ----------- |
|0,    | 1 |
|2,    | 3.3 |
|5.43, | 2342.34 |
|...  | ... |

 In every line one measurement is saved. There is an example in the *data/* folder :)

## Calculating the error funtions


Run the script *polynomial_regression.py* in the folder *scripts/* as follows:

~~~
python polynomial_regression.py <datafile> <degree>
e.g. from root folder: python scripts/polynomial_regression.py data/error_dist.csv 2
~~~

The degree parameter determines the largest degree of the polynomial. The printed values are the coefficients of the error polynomial.
