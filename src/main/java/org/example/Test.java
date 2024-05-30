package org.example;

public class Test {

    public static void main(String args[])
    {
       for(int i=1;i<=5;i++)
       {
           for(int j=1;j<=i;j++)
           {
               System.out.print(j);
           }
       }
System.out.println("myName is vijay singh ");
    }
public static int factorial(int n)
    {
        if(n==0)
        {
            return 1;
        }
        else
        {
            return n*factorial(n-1);
        }
    }
}
