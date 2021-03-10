package gin;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

import gin.edit.Edit;
import gin.test.InternalTestRunner;
import gin.test.UnitTestResult;
import gin.test.UnitTestResultSet;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;
import org.pmw.tinylog.Logger;

import com.sampullara.cli.Args;
import com.sampullara.cli.Argument;

import gin.edit.Edit.EditType;

/**
 * A handy utility for analysing patches. Not part of the main gin system.
 */
public class PatchAnalyser {

    private static final int REPS = 1;

    @Argument(alias = "f", description = "Required: Source filename", required = true)
    protected File source = null;

    @Argument(alias = "p", description = "Required: Patch description", required = true)
    protected String patchText = "|";

    @Argument(alias = "d", description = "Top directory")
    protected File packageDir;

    @Argument(alias = "c", description = "Class name")
    protected String className;

    @Argument(alias = "cp", description = "Classpath")
    protected String classPath;

    @Argument(alias = "t", description = "Test class name")
    protected String testClassName;

    @Argument(alias = "b", description = "Base directory of generated files")
    protected String baseDir = "";

    @Argument(alias = "id", description = "id of the generated patch")
    protected String id;


    private SourceFileLine sourceFileLine;
    private SourceFileTree sourceFileTree;
    private InternalTestRunner testRunner;

    // Instantiate a class and call search
    public static void main(String[] args) {
        PatchAnalyser analyser = new PatchAnalyser(args);
        analyser.analyse();
    }

    PatchAnalyser(String[] args) {

        Args.parseOrExit(this, args);

        this.sourceFileLine = new SourceFileLine(source.getAbsolutePath(), null);

        this.sourceFileTree = new SourceFileTree(source.getAbsolutePath(), null);
        if (this.packageDir == null) {
            this.packageDir = this.source.getParentFile().getAbsoluteFile();
        }
        if (this.classPath == null) {
            this.classPath = this.packageDir.getAbsolutePath();
        }
        if (this.className == null) {
            this.className = FilenameUtils.removeExtension(this.source.getName());
        }
        if (this.testClassName == null) {
            this.testClassName = this.className + "Test";
        }

    }

    private void analyse() {

        // Create SourceFile and tester classes, parse the patch and generate patched source.
        SourceFileLine sourceFileLine = new SourceFileLine(source.getAbsolutePath(), null);
        SourceFileTree sourceFileTree = new SourceFileTree(source.getAbsolutePath(), null);

        this.testRunner = new InternalTestRunner(className, classPath, testClassName);

        Patch patch = parsePatch(patchText, sourceFileLine, sourceFileTree);
        String patchedSource = patch.apply();

        // Write the patched source to file, for reference
        String patchedFilename = (id == null)
                ? baseDir + '/' + source + ".patched"
                : baseDir + '/' + id;
        try {
            FileUtils.writeStringToFile(new File(patchedFilename), patchedSource, Charset.defaultCharset());
        } catch (IOException e) {
            Logger.error("Could not write patched source to " + patchedFilename);
            Logger.trace(e);
            System.exit(-1);
        }

        // Evaluate patch
        UnitTestResultSet resultSet = testRunner.runTests(patch, REPS);

        // Output test results
        logTestResults(resultSet);

    }

    private static Patch parsePatch(String patchText, SourceFileLine sourceFileLine, SourceFileTree sourceFileTree) {

        if (patchText.equals("|")) {
//            Logger.info("No edits to be applied. Running original code.");
            Patch patch = new Patch(sourceFileTree);
            return patch;
        }

        List<Edit> editInstances = new ArrayList<>();

        String patchTrim = patchText.trim();
        String cleanPatch = patchTrim;

        if (patchTrim.startsWith("|")) {
            cleanPatch = patchText.replaceFirst("\\|", "").trim();
        }

        String[] editStrings = cleanPatch.trim().split("\\|");

        boolean allLineEdits = true;
        boolean allStatementEdits = true;

        for (String editString : editStrings) {

            String[] tokens = editString.trim().split("\\s+");

            String editAction = tokens[0];

            Class<?> clazz = null;

            try {
                clazz = Class.forName(editAction);
            } catch (ClassNotFoundException e) {
                Logger.error("Patch edit type unrecognised: " + editAction);
                Logger.trace(e);
                System.exit(-1);
            }

            Method parserMethod = null;
            try {
                parserMethod = clazz.getMethod("fromString", String.class);
            } catch (NoSuchMethodException e) {
                Logger.error("Patch edit type has no fromString method: " + clazz.getCanonicalName());
                Logger.trace(e);
                System.exit(-1);
            }

            Edit editInstance = null;
            try {
                editInstance = (Edit) parserMethod.invoke(null, editString.trim());
            } catch (IllegalAccessException e) {
                Logger.error("Cannot parse patch: access error invoking edit class.");
                Logger.trace(e);
                System.exit(-1);
            } catch (InvocationTargetException e) {
                Logger.error("Cannot parse patch: invocation error invoking edit class.");
                Logger.trace(e);
                System.exit(-1);
            }

            allLineEdits &= editInstance.getEditType() == EditType.LINE;
            allStatementEdits &= editInstance.getEditType() != EditType.LINE;
            editInstances.add(editInstance);

        }

        if (!allLineEdits && !allStatementEdits) {
            Logger.error("Cannot proceed: mixed line/statement edit types found in patch");
            System.exit(-1);
        }

        Patch patch = new Patch(allLineEdits ? sourceFileLine : sourceFileTree);
        for (Edit e : editInstances) {
            patch.add(e);
        }

        return patch;

    }

    private static void logTestResults(UnitTestResultSet results) {

//        Logger.info("Test Results");
//        Logger.info("Number of results: " + results.getResults().size());
//        Logger.info("Valid patch: " + results.getValidPatch());
//        Logger.info("Cleanly compiled: " + results.getCleanCompile());
        Logger.info("All tests successful: " + results.allTestsSuccessful());
//        Logger.info("Total execution time: " + results.totalExecutionTime());

//        for (UnitTestResult result : results.getResults()) {
//            Logger.info(result);
//        }

    }

}
