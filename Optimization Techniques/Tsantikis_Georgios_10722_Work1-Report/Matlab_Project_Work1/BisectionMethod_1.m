% ΘΕΜΑ 1 - ΜΕΘΟΔΟΣ ΤΗΣ ΔΙΧΟΤΟΜΟΥ (Αλγόριθμος 5.1.1)
clear 
close all
clc


% Συνάρτηση για την υλοποίηση της μεθόδου της διχοτόμησης που επιστρέφει το τελικό 
% διάστημα το οποίο περιέχει το ελάχιστο και τον αριθμό των επαναλήψεων k
function [intervals, iterations_cnt] = bisectionMethod(a, b, l, epsilon, f)
    a_k = a;
    b_k = b;
    iterations_cnt = 1;  % Ο μετρητής των επαναλήψεων
    intervals = [a, b];  % Αποθήκευση των άκρων του διαστήματος

    while (b_k - a_k > l)
        % Υπολογισμός των σημείων x1_k και x2_k (άκρα του νέου διαστήματος)
        x1_k = (a_k + b_k) / 2 - epsilon;
        x2_k = (a_k + b_k) / 2 + epsilon;

        % Υπολογισμός των τιμών της f στα σημεία x1_k και x2_k
        f_x1_k = f(x1_k);
        f_x2_k = f(x2_k);

        % Ανανέωση του διαστήματος σύμφωνα με το Βήμα 2 του αλγορίθμου
        if f_x1_k < f_x2_k
            b_k = x2_k;
        else
            a_k = x1_k;
        end

        % Αποθήκευση των νέων ορίων του διαστήματος
        intervals = [intervals; a_k, b_k];
        iterations_cnt = iterations_cnt + 1;
    end
end


% Οι αντικειμενικές συναρτήσεις για την εφαρμογή της παραπάνω μεθόδου
f1 = @(x) (x-2)^2 + x*log(x+3);
f2 = @(x) exp(-2*x) + (x-2)^2;
f3 = @(x) exp(x)*(x^3-1) + (x-1)*sin(x);

% Αρχικό διάστημα αναζήτησης [a b] και οι παράμετροι l, ε
a = -1;
b = 3;
epsilon_values = 0.001:0.0001:0.0049; % Η σταθερά ε με 2ε < l (απόσταση από τη διχοτόμο)
l_values = 0.0021:0.00025:0.0106; % Τελικό εύρος αναζήτησης
functions = {f1, f2, f3}; % Για την επιλογή των συναρτήσεων


% ΕΡΩΤΗΜΑ Α
l = 0.01; % Με σταθερό l
% Αρχικοποίηση για αποθήκευση του αριθμού υπολογισμών
num_calculations_per_function = zeros(length(functions), length(epsilon_values));
for i = 1:length(functions)
    f = functions{i}; % Επιλογή της αντικειμενικής συνάρτησης
    
    % Εφαρμογή της μεθόδου για διάφορες τιμές του ε
    for j = 1:length(epsilon_values)
        epsilon = epsilon_values(j);
        [intervals, iterations_cnt] = bisectionMethod(a, b, l, epsilon, f);
        num_calculations_per_function(i, j) = 2*iterations_cnt-2;
    end

    % Scatter Plot για τη συνάρτηση f_i
    figure;
    plot(epsilon_values, num_calculations_per_function(i, :), '-o', 'MarkerFaceColor', [0 0 1]);
    xlabel('\epsilon');
    ylabel('Αριθμός Υπολογισμών της f');
    title(['Μεταβολή Αριθμού Υπολογισμών για τη συνάρτηση f' num2str(i)])
end



% ΕΡΩΤΗΜΑΤΑ Β-Γ
epsilon = 0.001; % Με σταθερό ε
% Αρχικοποίηση για αποθήκευση του αριθμού υπολογισμών
num_calculations_per_function = zeros(length(functions), length(l_values));
for i = 1:length(functions)
    f = functions{i}; % Επιλογή της αντικειμενικής συνάρτησης
    
    figure;
    % Εφαρμογή της μεθόδου για διάφορες τιμές του l;
    for j = 1:length(l_values)
        l = l_values(j);
        [intervals, iterations_cnt] = bisectionMethod(a, b, l, epsilon, f);
        num_calculations_per_function(i, j) = 2*iterations_cnt;
        % Σχεδίαση γραφήματος για τα άκρα του διαστήματος [a_k, b_k]
        plot(1:iterations_cnt, intervals(:,1),'-o', 'DisplayName', ['a_k, l = ' num2str(l)]);
        hold on;
        plot(1:iterations_cnt, intervals(:,2),'-x', 'DisplayName', ['b_k, l = ' num2str(l)]);
    end
    xlabel('Επανάληψη k');
    ylabel('Τιμές άκρων');
    title(['Άκρα του διαστήματος για τη συνάρτηση f' num2str(i) ' με διαφορετικά l (ε = 0.001)']);
    hold off;

    % Scatter Plot για τη συνάρτηση f_i
    figure;
    plot(l_values, num_calculations_per_function(i, :), '-o', 'MarkerFaceColor', [1 0 0]);
    xlabel('l');
    ylabel('Αριθμός Υπολογισμών της f');
    title(['Μεταβολή Αριθμού Υπολογισμών για τη συνάρτηση f' num2str(i)])
end