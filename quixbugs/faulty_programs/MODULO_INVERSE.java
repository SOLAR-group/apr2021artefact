package faulty_programs;//Corrected package name from quixey to extra;
//package quixey;
/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author derricklin
 */
public class MODULO_INVERSE {
    public static int inverse(int base, int mod) {
            if(base == 1) {
            return base;
        } else {
            int coeff = base - inverse(mod % base, base);
            return (coeff*mod) / base;
        }
    }
}
