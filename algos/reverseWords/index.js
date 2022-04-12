/* 
Given a string containing space separated words
Reverse each word in the string.
If you need to, use .split to start, then try to do it without.
*/

const str1 = "hello";
const expected1 = "olleh";

const str2 = "hello world";
const expected2 = "olleh dlrow";

const str3 = "abc def ghi";
const expected3 = "cba fed ihg";

/**
 * Reverses the letters in each words in the given space separated
 * string of words. Does NOT reverse the order of the words themselves.
 * - Time: O(?).
 * - Space: O(?).
 * @param {string} str Contains space separated words.
 * @returns {string} The given string with each word's letters reversed.
 */
// function reverseWords(str) {
//     var newArr = []
//     var reverseStr = ""
//     str = str.split()
//     for (var i = 0; i <= str.length-1; i++){
//         if(str[i] != " "){
//             newArr += str[i]
//             console.log(newArr)
//         }
//         else{     
//             var reverseArr = newArr.reverse();
//             var joinArr = reverseArr.join();
//             console.log(joinArr)
//         }
//     }
//     return newArr
// }

function reversebyWords(str) {
    var words = [];
    words = str.match(/\S+/g);
    var result = "";
    for (var i = 0; i < words.length; i++) {
        result += words[i].split('').reverse().join('') + " ";
    }
    result = result.substring(0, result.length - 1);
    return result
}
console.log(reversebyWords(str1))
console.log(reversebyWords(str2))
console.log(reversebyWords(str3))

// module.exports = { reverseWords };