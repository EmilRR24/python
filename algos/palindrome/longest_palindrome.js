/* 
Longest Palindrome
For this challenge, we will look not only at the entire string provided,
but also at the substrings within it.
Return the longest palindromic substring. 
Strings longer or shorter than complete words are OK.
All the substrings of "abc" are:
a, ab, abc, b, bc, c
*/

const { isPalindrome  }= require("./is_palindrome");


const str1 = "what up, daddy-o?";
const expected1 = "dad";

const str2 = "uh, not much";
const expected2 = "u";

const str3 = "Yikes! my favorite racecar erupted!";
const expected3 = "e racecar e";

const str4 = "a1001x20002y5677765z";
const expected4 = "5677765";

const str5 = "a1001x20002y567765z";
const expected5 = "567765";

/**
 * Finds the longest palindromic substring in the given string.
 * - Time: O(?).
 * - Space: O(?).
 * @param {string} str
 * @returns {string} The longest palindromic substring from the given string.
 */
function longestPalindromicSubstring(str) {
    var lps = str[0];

    for(let i=0; i<str.length-1; i++){
        for(let j=i+2; j<=str.length; j++){
            var temp = str.substring(i,j)
            // console.log(temp)
            if(isPalindrome(temp)){
                if(temp.length > lps.length){
                    console.log("newlongest is", temp)
                    lps=temp;   
                }
            }
        }
    }
    return lps
}



console.log(longestPalindromicSubstring(str1))
console.log(longestPalindromicSubstring(str2))
console.log(longestPalindromicSubstring(str3))
console.log(longestPalindromicSubstring(str4))
console.log(longestPalindromicSubstring(str5))