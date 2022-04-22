/* 
  Array: Mode
  
  Create a function that, given an array of ints,
  returns the int that occurs most frequently in the array.
  What if there are multiple items that occur the same number of time?
    - return all of them (in an array)
    - what if all items occur the same number of times?
      - return empty array
*/

const nums1 = [];
const expected1 = [];

const nums2 = [1];
const expected2 = [1];

const nums3 = [5, 1, 4];
const expected3 = [];

const nums4 = [5, 1, 4, 1];
const expected4 = [1];

const nums5 = [5, 1, 4, 1, 5];
const expected5 = [5, 1];
//  - order doesn't matter

/**
 * Finds the mode or all modes if there are more than one. The mode is the
 *    value which occurs the most times in the given array.
 * - Time: O(?).
 * - Space: O(?).
 * @param {Array<number>} nums Test
 * @returns {Array<number>} Mode or modes in any order.
 */
function mode(nums) {
    if(nums.length < 2){
        return nums;
    }
    let freqTab = {};
    let count = 0;
    let highestFreq = []
    //Make frequency table
    for(let num of nums){
        if (freqTab[num]){
            freqTab[num]++;
        }
        else{
            freqTab[num] = 1;
        }
        //Find the Highest frequency
        if (freqTab[num] > count) {
            count = freqTab[num];
        }
    }
    //Find all keys that have the highest frequency and add to the new array
    for (let key in freqTab) {
        if (freqTab[key] ===  count) {
            highestFreq.push(parseInt(key));
        }
    }
    if(highestFreq.length === nums.length){
        return [];
    }
    return highestFreq
}

console.log(mode(nums1))
console.log(mode(nums2))
console.log(mode(nums3))
console.log(mode(nums4))
console.log(mode(nums5))