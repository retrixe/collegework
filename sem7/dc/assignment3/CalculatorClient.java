//Client Program which
//calls the remote services

//Client Program which
//calls the remote services

import java.rmi.Naming;
import java.rmi.RemoteException;
import java.net.MalformedURLException;
import java.rmi.NotBoundException;

public class CalculatorClient 
{

    public static void main(String[] args) 
    {
        try 
        {
	    int a,b;
		
            a=Integer.parseInt(args[0]);
            b=Integer.parseInt(args[1]);				
            CalculatorRI c = (CalculatorRI) 
                          Naming.lookup(
                "rmi://localhost/CalculatorService");
            System.out.println("a+b : "+ c.add(a, b) );
            System.out.println("a-b : "+ c.sub(a, b) );
            System.out.println("a*b : "+ c.mul(a, b) );
            System.out.println("a/b : "+ c.div(a, b) );
            System.out.println("a*a : "+ c.square(a) );
        }
	catch(ArrayIndexOutOfBoundsException e)
	{
		System.out.println("Sorry! insufficient arguments");
	}
        catch (MalformedURLException murle) 
        {
            System.out.println();
            System.out.println(
              "MalformedURLException");
            System.out.println(murle);
        }
        catch (RemoteException re) 
        {
            System.out.println();
            System.out.println(
                        "RemoteException");
            System.out.println(re);
        }
        catch (NotBoundException nbe) 
        {
            System.out.println();
            System.out.println(
                       "NotBoundException");
            System.out.println(nbe);
        }
        catch (java.lang.ArithmeticException ae) 
	{
            System.out.println();
            System.out.println(
             "java.lang.ArithmeticException");
            System.out.println(ae);
        }
    }
}