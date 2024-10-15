% Specify the folder containing the images
imageFolder = 'C:\Users\nithy\OneDrive\Desktop\Automatic_File_Deletion\good_morning'; % Change this to your folder path

% Create an image datastore
imds = imageDatastore(imageFolder);

ocrResults = cell(length(imds.Files), 1);
imageNames = imds.Files;  % Get the names of the images

for i = 1:length(imds.Files)
    img = read(imds);
    
    % Perform OCR
    ocrResults{i} = ocr(img);
    
    fprintf('Results for image %d:\n', i);
    disp(ocrResults{i}.Text);
end

% Extracted text
extractedText = cellfun(@(x) x.Text, ocrResults, 'UniformOutput', false);

% Save results to a text file
fileID = fopen('ocr_results.txt', 'w');
for i = 1:length(extractedText)
    fprintf(fileID, 'Image %d: %s\n', i, extractedText{i});
end
fclose(fileID);

% Analyze the word extraction and find images containing "Good Morning", "morning", or "GOOD MORNING"
searchPhrases = {'Good Morning', 'morning', 'GOOD MORNING'};
matchingImages = {};

for i = 1:length(extractedText)
    % Check for the presence of the search phrases in the extracted text
    for j = 1:length(searchPhrases)
        if contains(lower(extractedText{i}), lower(searchPhrases{j}))
            % Extract only the image name (without path)
            [~, imgName, ext] = fileparts(imageNames{i});
            matchingImages{end+1} = [imgName, ext]; %#ok<AGROW>
            break;  % No need to check other phrases for this image
        end
    end
end

% Display the image names containing the specified words
disp('Images containing "Good Morning", "morning", or "GOOD MORNING":');
disp(matchingImages);

% Calculate the count of matching images
matchingCount = length(matchingImages);
totalImages = length(imds.Files);

% Calculate the ratio
ratio = matchingCount / totalImages;

% Display the results
fprintf('Count of matching images: %d\n', matchingCount);
fprintf('Total number of images: %d\n', totalImages);
fprintf('Ratio of matching images to total images: %.2f\n', ratio);
