#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <cmath>

using namespace std;

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

string replace_string(string str, char subst){
    string result = "";
    for(int i=0; i<str.size(); i++){
        if(str[i] != subst){
            result += str[i];
        }
    }
    return result;
}

vector<int> get_int_string(string result){
    string delimiter = "x";
    size_t pos = 0;
    string token;
    vector<int> int_result;
    if((pos = result.find(delimiter)) < result.size()){
        token = result.substr(0, pos);
        // cout<<"token = "<<token<<"  token len = "<<token.size()<<" token='' "<<(token=="")<<endl;
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
        token = result.substr(pos + delimiter.length()+1);
        if (token.size() > 0){
            int_result.push_back(stoi(token));
        }else{
            int_result.push_back(1);
        }
    }
    else{
        // cout << result << " is not a valid string" << endl;
        // // cout<<"pos = "<<pos<<"  result.size() = "<<result.size()<<endl;
        // for(int j=0; j<result.size(); j++){
        //     cout<<j<<"="<<result[j]<<" ";
        // }
        int_result.push_back(stoi(result));
        int_result.push_back(0);
    }
    return int_result;
}



double func(vector<vector<int>> int_map, int x){
    double result = 0;
    for(int i=0; i<int_map.size(); i++){
        result += int_map[i][0] * pow(x, int_map[i][1]);
    }
    return result;
}

void bisections(vector<vector<int>> int_map, double a, double b, double epsilon){
    double c = (a+b)/2;
    double f_a = func(int_map, a);
    double f_c = func(int_map, c);
    double f_b = func(int_map, b);
    if(f_a*f_c < 0){}
    else if(f_a*f_b < 0){}
    else if(f_c*f_b < 0){}
    else{
        cout << "No solution" << endl;
        return;
    }
    while(abs(b-a) > epsilon){
        if(f_a*f_c < 0){
            b = c;
            f_b = f_c;
        }
        else if(f_a*f_b < 0){
            a = c;
            f_a = f_c;
        }
        else if(f_c*f_b < 0){
            b = c;
            f_b = f_c;
        }
        c = (a+b)/2;
        f_c = func(int_map, c);
    }
    cout << "x = " << c << endl;
}



int main(){

    string str;
    cout << "Enter the function: ";
    getline(cin, str);
    str = replace_string(str, ' ');
    str = replace_string(str, '^');

    cout << str << endl;
    vector<string> result = split_string(str);
    vector<vector<int>> int_map;
    for(int i=0; i<result.size(); i++){
        cout << result[i] << endl;
        vector<int> int_result = get_int_string(result[i]);
        int_map.push_back(int_result);
        for(int j=0; j<int_result.size(); j++){
            cout << int_result[j] << " ";
        }
        cout << endl;
    }
    double a, b, e;
    cout << "Enter a: ";
    cin >> a;
    cout << "Enter b: ";
    cin >> b;
    cout << "Enter e: ";
    cin >> e;
    bisections(int_map, a, b, e);
}


