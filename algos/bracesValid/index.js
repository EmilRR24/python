/* 
Braces Valid
Given a string sequence of parentheses, braces and brackets, determine whether it is valid. 
*/

const str1 = "W(a{t}s[o(n{ c}o)m]e )h[e{r}e]!";
const expected1 = true;

const str2 = "D(i{a}l[ t]o)n{e";
const expected2 = false;

const str3 = "A(1)s[O (n]0{t) 0}k";
const expected3 = false;

/**
 * Determines whether the string's braces, brackets, and parenthesis are valid
 * based on the order and amount of opening and closing pairs.
 * - Time: O(?).
 * - Space: O(?).
 * @param {string} str
 * @returns {boolean} Whether the given strings braces are valid.
 */
function bracesValid(str) {
    var count = 0;
    var count1 = 0;
    var count2 = 0;
    for (var i = 0; i < str.length; i++) {
        if(str[i] == "(" ){
            count += 1;
        }
        else if(str[i] == ")" ){
            count -= 1;
            if(count <0){
                return false;
            }
        }
    }
    for (var i = 0; i < str.length; i++) {
        if(str[i] == "[" ){
            count1 += 1;
        }
        else if(str[i] == "]" ){
            count1 -= 1;
            if(count1 <0){
                return false;
            }
        }
    }
    for (var i = 0; i < str.length; i++) {
        if(str[i] == "{" ){
            count2 += 1;
        }
        else if(str[i] == "}" ){
            count2 -= 1;
            if(count2 <0){
                return false;
            }
        }
    }
    if(count == 0 && count1 == 0 && count2 == 0) {
        return true;
    }
    else {
        return false;
    }
}

console.log(bracesValid(str1))
console.log(bracesValid(str2))
console.log(bracesValid(str3))