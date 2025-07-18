java version needs to be 8
you may install: jdk-8u202-windows-x64.exe

# go to project root directory using command prompt
cd jclust

# compile
del sources.txt
for /R src %f in (*.java) do @echo %f >> sources.txt
"C:\Program Files\Java\jdk1.8.0_202\bin\javac.exe" -cp "lib/*" -d bin @sources.txt

# help
C:\Users\Fidz\Downloads\jclust\jclust>java -cp "bin;lib/*" clustering.main.AlgorithmRunnerMain -help
usage: jclust
 -help                print this message
 -numthread <arg>     number of threads
 -outputlevel <arg>   output level (0,1,2,3)
 -paramfile <arg>     file name of the input data
 -prefix <arg>        file name prefix of the output data
 -vindex <arg>        validation index (e.g., RunTime:CorrectedRandIndex)

# update your kmodparam.csv inside kmod (datafolder, datafile, schemafile)

# make output folder
mkdir output

# run algorithms
java -Dlog4j.configurationFile=kmod/log4j2.xml -cp "bin;lib/*" clustering.main.AlgorithmRunnerMain ^
 -paramfile "kmod/kmodparam.csv" ^
 -prefix "output/output" ^
 -outputlevel 2 ^
 -numthread 1 ^
 -vindex "RunTime:CorrectedRandIndex"




# PYTHON boxplotting
# install dependencies
pip install pandas matplotlib seaborn
