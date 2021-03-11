package faulty_programs;

public class HANOI_TEST {
    @org.junit.Test(timeout = 3000)
    public void test_0() throws Exception {
        java.util.List result = HANOI.hanoi((int)1,(int)1,(int)3);
        String resultFormatted = QuixFixOracleHelper.format(result,true);
        org.junit.Assert.assertEquals("[[1,3]]", resultFormatted);
    }

    @org.junit.Test(timeout = 3000)
    public void test_1() throws Exception {
        java.util.List result = HANOI.hanoi((int)2,(int)1,(int)3);
        String resultFormatted = QuixFixOracleHelper.format(result,true);
        org.junit.Assert.assertEquals("[[1,2],[1,3],[2,3]]", resultFormatted);
    }

    @org.junit.Test(timeout = 3000)
    public void test_2() throws Exception {
        java.util.List result = HANOI.hanoi((int)3,(int)1,(int)3);
        String resultFormatted = QuixFixOracleHelper.format(result,true);
        org.junit.Assert.assertEquals("[[1,3],[1,2],[3,2],[1,3],[2,1],[2,3],[1,3]]", resultFormatted);
    }

    @org.junit.Test(timeout = 3000)
    public void test_3() throws Exception {
        java.util.List result = HANOI.hanoi((int)4,(int)1,(int)3);
        String resultFormatted = QuixFixOracleHelper.format(result,true);
        org.junit.Assert.assertEquals("[[1,2],[1,3],[2,3],[1,2],[3,1],[3,2],[1,2],[1,3],[2,3],[2,1],[3,1],[2,3],[1,2],[1,3],[2,3]]", resultFormatted);
    }

    @org.junit.Test(timeout = 3000)
    public void test_4() throws Exception {
        java.util.List result = HANOI.hanoi((int)2,(int)1,(int)2);
        String resultFormatted = QuixFixOracleHelper.format(result,true);
        org.junit.Assert.assertEquals("[[1,3],[1,2],[3,2]]", resultFormatted);
    }

    @org.junit.Test(timeout = 3000)
    public void test_5() throws Exception {
        java.util.List result = HANOI.hanoi((int)2,(int)1,(int)1);
        String resultFormatted = QuixFixOracleHelper.format(result,true);
        org.junit.Assert.assertEquals("[[1,2],[1,1],[2,1]]", resultFormatted);
    }

    @org.junit.Test(timeout = 3000)
    public void test_6() throws Exception {
        java.util.List result = HANOI.hanoi((int)2,(int)3,(int)1);
        String resultFormatted = QuixFixOracleHelper.format(result,true);
        org.junit.Assert.assertEquals("[[3,2],[3,1],[2,1]]", resultFormatted);
    }
//evosuite
  @Test(timeout = 4000)
  public void test7()  throws Throwable  {
      List<HANOI.Pair<Integer, Integer>> list0 = HANOI.hanoi(3, 515, (-2928));
      assertEquals(7, list0.size());
  }

  @Test(timeout = 4000)
  public void test8()  throws Throwable  {
      HANOI hANOI0 = new HANOI();
  }

  @Test(timeout = 4000)
  public void test9()  throws Throwable  {
      Integer integer0 = new Integer(756);
      HANOI.Pair<Integer, Integer> hANOI_Pair0 = new HANOI.Pair<Integer, Integer>(integer0, integer0);
      Integer integer1 = hANOI_Pair0.getFirst();
      assertEquals(756, (int)integer1);
  }

  @Test(timeout = 4000)
  public void test10()  throws Throwable  {
      HANOI.Pair<String, String> hANOI_Pair0 = new HANOI.Pair<String, String>(" bjuqKH86b;1;B", " bjuqKH86b;1;B");
      Object object0 = hANOI_Pair0.getSecond();
      assertEquals(" bjuqKH86b;1;B", object0);
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      HANOI.Pair<String, String> hANOI_Pair0 = new HANOI.Pair<String, String>(" bjuqKH86b;1;B", " bjuqKH86b;1;B");
      hANOI_Pair0.setFirst("");
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      List<HANOI.Pair<Integer, Integer>> list0 = HANOI.hanoi((-1335), 2555, (-1335));
      HANOI.Pair<Object, String> hANOI_Pair0 = new HANOI.Pair<Object, String>(list0, "BDwU8uL3$SNvyL[");
      String string0 = hANOI_Pair0.toString();
      assertEquals("([], BDwU8uL3$SNvyL[)", string0);
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      HANOI.Pair<String, Integer> hANOI_Pair0 = new HANOI.Pair<String, Integer>("", (Integer) null);
      hANOI_Pair0.setSecond((Integer) null);
  }
}

