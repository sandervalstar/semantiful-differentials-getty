# Getty - Semantiful Differentials

Getty is a tool to support Continuous Semantic Inspection (CSI) for Java projects.

### *Continuous Semantic Inspection*
CSI is a process for developers to inspect behavioral changes before patching the system. 
In addition to source code changes, developers are suggested to review semantic change summaries. 
Like Continuous Integration (CI) that supports effortless testing, CSI provides change summaries with little effort from developers.

### *System Requirement*
  * Operating System:
    *  Unix-like systems (e.g., Mac OS X, 10.10.5+)
    *  Linux family (e.g., Ubuntu 14.04+)
    *  Windows 10 Editions, 64-bit with Bash shell (Windows Subsystem for Linux)
  * Programming Languages and Tools:
    * [Java (SDK 7)](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html) and [Maven (3.x)](https://maven.apache.org/)
    * [Python (2.7.x)](https://www.python.org/)
  * Version Control System:
    * [Git 2.2.x](https://git-scm.com/)

### *Applicable Projects*
The projects Getty can analyze should satisfy the following criteria:
  * Written in Java
  * Built by Maven (single-module\* setting)
  * Configured to test using JUnit (version 3 or 4) only

\*Disclaimer of [Maven multi-module](https://maven.apache.org/guides/mini/guide-multiple-modules.html) project support - The mechanism (reactor) in Maven that handles multi-module projects collects all available modules (sub-projects), sorts and builds all selected ones in their correct build order. The use of multiple modules remains controversal ([discussion in reddit](https://www.reddit.com/r/programming/comments/1ns6ae/maven_is_broken_by_design/?st=itjkarzb&sh=4aee9c04), [discussion in stackoverflow](http://stackoverflow.com/questions/11730791/why-and-when-to-create-a-multi-module-maven-project), etc.). As a more general case, Getty targets single-module Maven projects. Though Getty does not provide direct support towards multi-module projects, however, you can still analyze each of their included single modules separately.

### *Prep*
  * Confirm system requirements are met: all executables should be set on your path and you can run them __without specifying full path__. For example:
  
  ```bash
  $ java -version
  java version "1.7.0_71"
  Java(TM) SE Runtime Environment (build 1.7.0_71-b14)
  Java HotSpot(TM) 64-Bit Server VM (build 24.71-b01, mixed mode)
  
  $ mvn -v
  Apache Maven 3.2.1 (ea8b2b07643dbb1b84b6d16e1f08391b666bc1e9; 2014-02-14T09:37:52-08:00)
  Maven home: /Users/myusername/path/to/maven
  Java version: 1.7.0_71, vendor: Oracle Corporation
  Java home: /Library/Java/JavaVirtualMachines/jdk1.7.0_71.jdk/Contents/Home/jre
  Default locale: en_US, platform encoding: UTF-8
  OS name: "mac os x", version: "10.11.5", arch: "x86_64", family: "mac"
  
  $ python --version
  Python 2.7.11
  
  $ git --version
  git version 2.2.1
  ```

### *Using Getty*
  * Clone Getty project, choose your own `/path/to/your/Getty/`. After this step you should see a directory named `semantiful-differentials-getty`
  
  ```bash
  $ cd /path/to/your/Getty/
  $ git clone https://github.com/ybank/semantiful-differentials-getty.git
  ```
  
  * If you are using Eclipse, the project should build automatically and the built version of CSI is under the subdirectory `bin/`. Otherwise, and more generally, you can use the path to CSI in source: `getty/csi`. The following example use the latter case.
  
  ```bash
  $ /path/to/your/Getty/semantiful-differentials-getty/getty/csi --help
  villa.jar path: /your/path/to/villa.jar
  junit-x-getty.jar path: /your/path/to/junit-4.13-getty.jar
  jdyncg-0.1-getty-dycg-agent.jar path: /your/path/to/jdyncg-0.4-getty-dycg-agent.jar
  
  == Usage ==
  
  	Get help:
  	  csi < -h | --help >
  
  	Default compare: origin/HEAD or origin/master or origin/trunk vs. HEAD:
  	  csi
  
  	Compare HEAD with the given commit, or with the commit of given ancestor index:
  	  csi < commit | -index >
  
  	Compare between the given commits: preimage_commit vs. postimage_commit (give issue name optionally):
  	  csi < preimage_commit > < postimage_commit > [issue:<ISSUE_NAME>]
  	  csi < ~relative_index > < postimage_commit > [issue:<ISSUE_NAME>]
  	  csi < -preimage_index > < -postimage_index > [issue:<ISSUE_NAME>]
  	  csi < preimage_commit > < postimage_commit > -i
  ```

  * Clone the project to analyze. For example, get the following example project:
  
  ```bash
  $ git clone https://github.com/ybank/dsproj.git
  ```
  
  * Go to the project's working directory. (For a multi-module project, go to its specific single module's working directory; for example, Google's GSON project has multiple modules so the user should go to `gson/gson` subdirectory if she is interested in the `gson` sub-module.)
  ```bash
  $ cd dsproj
  ```
  
  * Review invariant differentials between any two commits! As an example, compare commit `a562db1` to one of its ancestor commits (`19f4281`) of the example project.
  
  ```bash
  $ /path/to/your/Getty/semantiful-differentials-getty/getty/csi 19f4281 a562db1
  ```
  By default, Getty does not isolate invariant changes due to different types of code update. More frequently, however, it is necessary to let Getty isolate the impact of source or test code changes. To get the integrated impact-isolated view (superset of the results above), append the option `-i` at the end of the commend.
  ```bash
  $ /path/to/your/Getty/semantiful-differentials-getty/getty/csi ~1 19f4281 a562db1 -i
  ```
  
  After analysis your terminal will tell you where to look at the results. 
  The default location is:
  
    `/path/to/your/example/project.__getty_output__/sema.diff.html`
  
  Or, for isolated view, the location is:
  
    `/path/to/your/example/project.__getty_output__/iso_$PREV_$POST/sema.diff.html`
  
  In the above path, `$PREV` is the first commit hash passed in command line and `$POST` the second; for example, the results of the isolated view by the last command above is located at:
  
    `/path/to/your/example/project.__getty_output__/iso_19f4281_a562db1/sema.diff.html`
  
  [This UI demo](http://sosa01.ucsd.edu:8000/sema.diff.html) shows the above view. For best viewing results, [Firefox](https://www.mozilla.org/en-US/firefox/new/), [Safari](http://www.apple.com/safari/) and [Chrome](https://www.google.com/chrome/) are recommanded to open the rendered html pages. On Windows 10, [Internet Explorer](https://www.microsoft.com/en-us/download/internet-explorer.aspx) and [Edge](https://www.microsoft.com/en-us/windows/microsoft-edge) are also good to open and view results.
  
  That's it!

### *Demos & Misc*
[Here](http://sosa08.ucsd.edu:7999/sema.diff.html) is an *outdated* demo of the source-impact isolated CSI view, for the commit ("#7", the introductory commit) we discussed in our submitted ICSE paper under review. If the reviewers are interested in the case study in the paper, here is [our latest user interface](http://sosa08.ucsd.edu:8000/sema.diff.html) displayed for commit #4, the commit that actually introduced the "equals" bug we discussed in the paper.

Please note that our latest user interface has been changed moderately (a refined UI style, more enriched features and integration of impact-isolated views) with updated Daikon library, but most other part of the UI resembles the past.

We have also updated the textual-diffing algorithm for invariant matching, which gives slightly cleaner diffing results; but ideally, we would like to further enhance it to a real semantic diffing algorithm backed by a theorem prover, which is currently WIP for future applications.
  
### *Support*
Please send email to the authors ({yayan, mmenarini, wgg} 'AT' cs 'dot' ucsd 'dot' edu) to discuss Getty, or to post questions.
