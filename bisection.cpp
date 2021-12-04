#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <cmath>

using namespace std;


// spliting string into vector of strings(by delimiter[-,+])
vector<string> split_string(string str){
    vector<string> result;
    string sub_s="";
    for(int i=0; i<str.size(); i++){
        if(str[i] == '-'){
            if(i == 0){
                sub_s += str[i];
            }
            else{
                result.push_back(sub_s);
                sub_s = "-";
            }
        }
        else if(str[i] == '+'){
            if(i == 0){
                sub_s += str[i];
            }
            else{
                result.push_back(sub_s);
                sub_s = "+";
            }
        }
        else{
            sub_s += str[i];
        }
    }
    if (sub_s != ""){
        result.push_back(sub_s);
    }
    return result;
}


// string char replace [" ","^"] -> ["",""]
string replace_string(string str, char subst){
    string result = "";
    for(int i=0; i<str.size(); i++){
        if(str[i] != subst){
            result += str[i];
        }
    }
    return result;
}


// get coefficient of x and also get power of x
vector<int> get_int_string(string result){
    string delimiter = "x";
    size_t pos = 0;
    string token;
    vector<int> int_result;
    if((pos = result.find(delimiter)) < result.size()){
        token = result.substr(0, pos);
        if(token == "+"){
            int_result.push_back(1);
        }
        else if(token == "-"){
            int_result.push_back(-1);
        }
        else if(token == ""){
            int_result.push_back(1);
        }
        else{
            int_result.push_back(stoi(token));
        }
        token = result.substr(pos + delimiter.length());
        if (token.size() > 0){
            int_result.push_back(stoi(token));
        }else{
            int_result.push_back(1);
        }
    }
    else{
        int_result.push_back(stoi(result));
        int_result.push_back(0);
    }
    return int_result;
}


// Equation of given string
double func(vector<vector<int>> int_map, double x){
    double result = 0;
    for(int i=0; i<int_map.size(); i++){
        result += int_map[i][0] * pow(x, int_map[i][1]);
    }
    return result;
}


// Bisection method
void bisections(vector<vector<int>> int_map, double a, double b, double epsilon){
    double c, f_a, f_b, f_c;
    f_a = func(int_map, a);
    f_b = func(int_map, b);

    if(f_a*f_b >= 0){
        cout << "No solution" << endl;
        return;
    }
    while(abs(b-a) > epsilon){
        //Find middle point
        c = (a+b)/2;

        f_c = func(int_map, c);

        //If f_c == 0 that means we got solution
        if(f_c==0.0)break;

        //If f_a and f_c have different signs, then we have to move left side of interval
        if(f_a*f_c < 0){
            b = c;
        }
        else{
            a = c;
            f_a = f_c;
        }
    }
    cout << "Value of root: " << c << endl;
}



int main(){

    string str;
    cout << "Enter the function: ";
    getline(cin, str);
    
    double a, b, e;
    cout << "Enter a: ";
    cin >> a;
    cout << "Enter b: ";
    cin >> b;
    cout << "Enter e: ";
    cin >> e;

    // string char replace [" ","^"] -> ["",""]
    str = replace_string(str, ' ');
    str = replace_string(str, '^');

    // spliting string into vector of strings(by delimiter[-,+])
    vector<string> result = split_string(str);

    // get coefficient of x and also get power of x
    vector<vector<int>> int_map;
    for(int i=0; i<result.size(); i++){
        vector<int> int_result = get_int_string(result[i]);
        int_map.push_back(int_result);
    }
    bisections(int_map, a, b, e);
    return 0;
}
