package edu.ucsd.getty.comp;

import static org.junit.Assert.*;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.junit.Test;

import edu.ucsd.getty.IMethodRecognizer;
import edu.ucsd.getty.comp.ASTInspector;

public class ASTInspectorTest {

	@Test
	public void testOneFileOneLine() {
		IMethodRecognizer recognizer = new ASTInspector();
		Map<String, Integer[]> diffs = new HashMap<String, Integer[]>();
		diffs.put("java/test/data/src/TestjavaSource.java.file", new Integer[]{39});
		Set<String> expected = new HashSet<String>();
		expected.add("some.pack.TestJavaSource$ReadMeIn:innerMethod-36");
		assertEquals(expected, recognizer.changedMethods(diffs));
	}
	
	@Test
	public void testOneFileMultipleLinesOneResult() {
		IMethodRecognizer recognizer = new ASTInspector();
		Map<String, Integer[]> diffs = new HashMap<String, Integer[]>();
		diffs.put("java/test/data/src/TestJavaSource.java.file", new Integer[]{38, 39, 40});
		Set<String> expected = new HashSet<String>();
		expected.add("some.pack.TestJavaSource$ReadMeIn:innerMethod-36");
		assertEquals(expected, recognizer.changedMethods(diffs));
	}
	
	@Test
	public void testOneFileMultipleLinesMultipleResults() {
		IMethodRecognizer recognizer = new ASTInspector();
		Map<String, Integer[]> diffs = new HashMap<String, Integer[]>();
		diffs.put("java/test/data/src/TestJavaSource.java.file", new Integer[]{
				10, 11, 20, 21, 38, 39, 40});
		Set<String> expected = new HashSet<String>();
		expected.add("some.pack.TestJavaSource$ReadMeIn:innerMethod-36");
		expected.add("some.pack.TestJavaSource:main-12");
		assertEquals(expected, recognizer.changedMethods(diffs));
	}
	
	@Test
	public void testMultipleFilesMultipleLinesMultipleResults() {
		IMethodRecognizer recognizer = new ASTInspector();
		Map<String, Integer[]> diffs = new HashMap<String, Integer[]>();
		diffs.put("java/test/data/src/TestJavaSource.java.file", new Integer[]{
				10, 11, 20, 21, 38, 39, 40});
		diffs.put("java/test/data/src/TestJavaSource2.java.file", new Integer[]{
				14, 15, 16, 17, 100});
		Set<String> expected = new HashSet<String>();
		expected.add("some.pack.TestJavaSource$ReadMeIn:innerMethod-36");
		expected.add("some.pack.TestJavaSource:main-12");
		expected.add("some.pack2.TestJavaSource2:someMethod-12");
		expected.add("some.pack2.TestJavaSource2:anotherMethod-16");
		assertEquals(expected, recognizer.changedMethods(diffs));
	}
	
	@Test
	public void testDeclarationLineNumberSingleFileInformation() {
		Map<String, Integer> results = ASTInspector.getMethodLineNumberMap(
				"java/test/data/src/RealEnumTest.java.file", ".java.file");
		assertEquals(3, results.keySet().size());
		assertEquals(15, (int) results.get("com.crunchify.tutorials.CrunchifyEnumExample:<init>-15"));
		assertEquals(19, (int) results.get("com.crunchify.tutorials.CrunchifyEnumExample:companyDetails-19"));
		assertEquals(40, (int) results.get("com.crunchify.tutorials.CrunchifyEnumExample:main-40"));
	}
	
	@Test
	public void testDeclarationLineNumberDirectoryInformation() {
		Map<String, Integer> results = ASTInspector.getMethodLineNumberMap(
				"java/test/data", ".java.file");
		assertEquals(47, results.keySet().size());
	}

}
