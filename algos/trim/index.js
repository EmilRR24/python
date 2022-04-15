/* 
  Given a string that may have extra spaces at the start and the end,
  return a new string that has the extra spaces at the start and the end trimmed (removed)
  do not remove any other spaces.
*/

const str1 = "   hello world     ";
const expected1 = "hello world";

const str2 = "\n hello world "

/**
 * Trims any leading or trailing white space from the given str.
 * - Time: O(?).
 * - Space: O(?).
 * @param {string} str
 * @returns {string} The given string with any leading or trailing white space
 *    stripped.
 */
function trim(str) {
    var sInd = 0;
    var eInd = str.length - 1;
    while( str[sInd] == false) {
        sInd++;
        // counting up whitespace from index 0 until we reach a character
    }
    // console.log(sInd)
    while( str[eInd] == false) {
        eInd--;
        // counting down whitespace from index str.length-1 until we reach a character
    }
    eInd++;
    // to incluse the last character prior to being sliced
    // console.log(eInd)
    retStr = str.slice(sInd, eInd)
    // new string the white spaces removed
    return retStr
}
console.log(trim(str1))
console.log(trim(str2))