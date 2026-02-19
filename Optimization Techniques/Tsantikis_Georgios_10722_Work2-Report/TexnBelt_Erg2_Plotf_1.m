% ΘΕΜΑ 1 - ΣΧΕΔΙΑΣΗ ΤΗΣ ΣΥΝΑΡΤΗΣΗΣ f
clear 
close all
clc

syms x y

% Ορισμός της συνάρτησης
f = x^5 * exp(-x^2 - y^2);

% Υπολογισμός μερικών παραγώγων
df_dx = diff(f, x);
df_dy = diff(f, y);

% Εύρεση κρίσιμων σημείων (df/dx = 0 και df/dy = 0)
[crit_x, crit_y] = solve([df_dx == 0, df_dy == 0], [x, y]);

% Εύρεση δευτέρων παραγώγων
d2f_dx2 = diff(df_dx, x);
d2f_dy2 = diff(df_dy, y);
d2f_dxdy = diff(df_dx, y);

% Υπολογισμός του διακριτού τελεστή D
D = d2f_dx2 * d2f_dy2 - d2f_dxdy^2;

% Κατάταξη των κρίσιμων σημείων
critical_points = [crit_x, crit_y];
disp('Κρίσιμα σημεία:');
disp(critical_points);

for i = 1:length(crit_x)
    x0 = crit_x(i);
    y0 = crit_y(i);
    
    % Υπολογισμός του διακριτού τελεστή D στο κρίσιμο σημείο
    D_value = subs(D, [x, y], [x0, y0]);
    f_xx = subs(d2f_dx2, [x, y], [x0, y0]);
    
    if D_value > 0
        if f_xx > 0
            fprintf('Το σημείο (%.4f, %.4f) είναι τοπικό ελάχιστο.\n', x0, y0);
        else
            fprintf('Το σημείο (%.4f, %.4f) είναι τοπικό μέγιστο.\n', x0, y0);
        end
    elseif D_value < 0
        fprintf('Το σημείο (%.4f, %.4f) είναι σημείο σάγματος.\n', x0, y0);
    else
        fprintf('Για το σημείο (%.4f, %.4f) χρειάζεται να ελέγξουμε την γεωμετρία της συνάρτησης γύρω από αυτό.\n', x0, y0);
    end
end

% Σχεδίαση της συνάρτησης
figure(19)
fsurf(matlabFunction(f), [-3 3 -3 3])

% Προσθήκη κρίσιμων σημείων στη γραφική
hold on
for i = 1:length(crit_x)
    plot3(double(crit_x(i)), double(crit_y(i)), ...
        double(subs(f, [x, y], [crit_x(i), crit_y(i)])), 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
end
hold off