#include <cstring>
#include <memory>
#include <math.h>
#include "Python.h"

typedef int pynum_t;


template<class T> T max(T a, T b) { return a > b ? a : b; }

#define TBL_VAL(r, c) (table[(c)*rows + (r)])

#define USE_PYMEM 1

#if USE_PYMEM == 1
#include "pymem.h"


#define MY_MALLOC PyMem_Malloc
#define MY_FREE PyMem_Free

#else

#define MY_MALLOC malloc 
#define MY_FREE free 

#endif

extern "C" {

#ifdef _MSCVER

__declspec(dllexport)

#endif

char *solve_it(char *inputData)
{
   pynum_t *values;
   pynum_t *weights;


   /* Parse the first line */
   char *line = strtok(inputData, "\r\n");

   if (line == nullptr) {
      puts("ERROR: input file malformed");
      return nullptr;
   }

   char *pSpace;

   const int numItems = strtoul(line, &pSpace, 10);
   const pynum_t capacity = strtoul(pSpace, nullptr, 10);
   line = strtok(nullptr, "\r\n");

   values = (pynum_t *)MY_MALLOC(sizeof(pynum_t)*numItems);
   weights = (pynum_t *)MY_MALLOC(sizeof(pynum_t)*numItems);
   
   /* Parse the rest of the data */
   int itemNum = 0;
   while(line != nullptr) {
      values[itemNum] = strtoul(line, &pSpace, 10);
      weights[itemNum] = strtoul(pSpace, nullptr, 10);

      ++itemNum;
      line = strtok(nullptr, "\r\n");
   }
  
   pynum_t rows = capacity + 1;
   pynum_t cols = numItems + 1;

   puts("Initializing table...");

   pynum_t *table = (pynum_t *)MY_MALLOC(sizeof(pynum_t) * rows * cols);
      
   /* Zero out the first row and colum */
   for (pynum_t col = 0; col < cols; ++col) {
      TBL_VAL(0, col) = 0;
   }

   for (pynum_t row = 0; row < rows; ++row) {
      TBL_VAL(row, 0) = 0;
   }

   puts("Done initializing table...\n");

   /* Build the table */
   puts("Building Table...");
   for (pynum_t col = 1; col < cols; ++col) {
      for (pynum_t row = 1; row < rows; ++row) {
         TBL_VAL(row, col) = 
            weights[col-1] <= row ?
               max(TBL_VAL(row, col-1), values[col-1] + TBL_VAL(row - weights[col-1], col-1)) :
               TBL_VAL(row, col-1);
      }
   }
   puts("Done building table.\n");
   

   //puts("Table:");
   //for (pynum_t row = 0; row < rows; ++row) {
   //   fputs("|", stdout);
   //   for (pynum_t col = 0; col < cols-1; ++col) {
   //      printf("%llu, ", TBL_VAL(row, col));
   //   }
   //   printf("%llu", TBL_VAL(row, cols-1));
   //   fputs("|\n", stdout);
   //}
   
   puts("\nTracking backward...");
   pynum_t weightRem = capacity;
   itemNum = (int)(numItems-1);
   while (itemNum >= 0) {
      if (TBL_VAL(weightRem, itemNum) != TBL_VAL(weightRem, itemNum+1)) {
         values[itemNum] = 1;
         weightRem -= weights[itemNum];
      } else {
         values[itemNum] = 0;
      }

      // printf("\tAssigning item %llu = %llu\n", itemNum, values[itemNum]);
      --itemNum;
   }
   puts("Done tracking backward.\n");

   /* Build the solution string.  
      Remember that the 'taken' value for each item is stored in values.
      Estimate the string length based on a generous guess
   */

   char *retString = (char *)MY_MALLOC(sizeof(char) * (100 + 100*numItems));

   if (retString == nullptr) {
      puts("ERROR: Couldn't allocate return string.");
      return nullptr; 
   }

   puts("Writing solution string...");
   int written = sprintf(retString, "%llu 1\n", TBL_VAL(rows-1, cols-1));
   
   for (itemNum = 0; itemNum < numItems; ++itemNum) {
      written += sprintf((retString+written), "%llu ", values[itemNum]);
   }
   retString[written] = '\0';
   puts("Done writing solution string...\n");

   MY_FREE(weights);
   MY_FREE(values);
   MY_FREE(table);
   return retString;
}

}
