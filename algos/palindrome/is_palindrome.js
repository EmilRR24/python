/* 
String: Is Palindrome
Create a function that returns a boolean whether the string is a strict palindrome. 
    - palindrome = string that is same forwards and backwards

Do not ignore spaces, punctuation and capitalization
 */

const str1 = "a x a";
const expected1 = true;

const str2 = "racecar";
const expected2 = true;

const str3 = "Dud";
const expected3 = false;

const str4 = "oho!";
const expected4 = false;


/**
 * Determines if the given str is a palindrome (same forwards and backwards).
 * - Time: O(?).
 * - Space: O(?).
 * @param {string} str
 * @returns {boolean} Whether the given str is a palindrome or not.
 */
function isPalindrome(str) {
    var newStr = [] // create new string to hold palindrome string
    for(i=str.length -1; i >= 0; i--){ 
        newStr.push(str[i]) // loop through each character in string and add to the new string each character
    }
    newStr = newStr.toString() // changes new string from an array to a string
    newStr = newStr.replace(/,/g,'') // removes the " , " created by being in an array
    // console.log(newStr)
    if(newStr === str){ // boolean to see if new string equals string
        console.log(true)
        return true
    }
    else{
        console.log(false)
        return false
    }
}

console.log(isPalindrome(str1));
console.log(isPalindrome(str2));
console.log(isPalindrome(str3));
console.log(isPalindrome(str4));

// DONT CHANGE ANYTHING BELOW THIS LINE !!!!

module.exports = { isPalindrome };
