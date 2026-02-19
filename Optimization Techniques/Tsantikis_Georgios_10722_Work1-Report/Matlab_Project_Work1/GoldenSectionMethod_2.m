% ΘΕΜΑ 2 - ΜΕΘΟΔΟΣ ΤΟΥ ΧΡΥΣΟΥ ΤΟΜΕΑ (Αλγόριθμος 5.1.2)
clear 
close all
clc


% Συνάρτηση για την υλοποίηση της μεθόδου του χρυσού τομέα που επιστρέφει το τελικό 
% διάστημα το οποίο περιέχει το ελάχιστο και τον αριθμό των επαναλήψεων k
function [intervals, iterations_cnt] = goldenSectionMethod(a, b, l, f)    
    gamma = 0.618; % Η χρυσή τομή
    iterations_cnt = 1;  % Ο μετρητής των επαναλήψεων
    intervals = [a, b];  % Αποθήκευση των άκρων του διαστήματος

    % Στην πρώτη επανάληψη χρειάζονται οι υπολογισμοί και των δύο εσωτερικών
    % σημείων, ενώ στις επόμενες θα υπολογίζω μόνο ένα από τα δυο 
    x1 = a + (1-gamma)*(b - a);
    x2 = a + gamma*(b - a);
    % Υπολογισμός των τιμών της f στα σημεία x11 και x21
    f_x1 = f(x1);
    f_x2 = f(x2);

    % Επαναληπτική διαδικασία εύρεσης των νέων διαστημάτων
    while (b - a > l)
        if f_x1 < f_x2
            % Ανανέωση του διαστήματος σε [a, x2]
            b = x2;
            x2 = x1;
            f_x2 = f_x1;
            x1 = a + (1-gamma)*(b - a);
            f_x1 = f(x1);
        else 
            % Ανανέωση του διαστήματος σε [x1, b]
            a = x1;
            x1 = x2;
            f_x1 = f_x2;
            x2 = a + gamma*(b - a);
            f_x2 = f(x2);
        end

        % Αποθήκευση των νέων ορίων του διαστήματος
        intervals = [intervals; a, b];
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
l_values = 0.0021:0.00025:0.0106; % Τελικό εύρος αναζήτησης
functions = {f1, f2, f3}; % Για την επιλογή των συναρτήσεων


% ΕΡΩΤΗΜΑΤΑ
% Αρχικοποίηση για αποθήκευση του αριθμού υπολογισμών
num_calculations_per_function = zeros(length(functions), length(l_values));
for i = 1:length(functions)
    f = functions{i}; % Επιλογή της αντικειμενικής συνάρτησης
    
    figure;
    % Εφαρμογή της μεθόδου για διάφορες τιμές του l;
    for j = 1:length(l_values)
        l = l_values(j);
        [intervals, iterations_cnt] = goldenSectionMethod(a, b, l, f);
        num_calculations_per_function(i, j) = 1+ iterations_cnt;
        % Σχεδίαση γραφήματος για τα άκρα του διαστήματος [a_k, b_k]
        plot(1:size(intervals, 1), intervals(:,1),'-o', 'DisplayName', ['a_k, l = ' num2str(l)]);
        hold on;
        plot(1:size(intervals, 1), intervals(:,2),'-x', 'DisplayName', ['b_k, l = ' num2str(l)]);
    end
    xlabel('Επανάληψη k');
    ylabel('Τιμές άκρων');
    title(['Άκρα του διαστήματος για τη συνάρτηση f' num2str(i) ' με διαφορετικά l (ε = 0.001)']);
    hold off;

    % Plot για τη συνάρτηση f_i
    figure;
    plot(l_values, num_calculations_per_function(i, :), '-o', 'MarkerFaceColor', [1 0 0]);
    xlabel('l');
    ylabel('Αριθμός Υπολογισμών της f');
    title(['Μεταβολή Αριθμού Υπολογισμών για τη συνάρτηση f' num2str(i)])
end