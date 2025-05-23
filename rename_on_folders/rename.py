import anchorpoint as ap
import os
import re

def sort_files(files):
    # Sort by the base filename (without extension), then by extension
    return sorted(files, key=lambda f: os.path.splitext(os.path.basename(f))[0])

def batch_rename(selected_files, base_folder, in_subfolder=True):
    progress = ap.Progress("Renaming Files", infinite=False)
    progress.set_cancelable(True)

    total_files = len(selected_files)
    renamed_count = 0

    

    try:
        base_folder_name = os.path.basename(base_folder)  # Get the name of the base folder
        
        # Determine parent and grandparent folder based on in_subfolder option
        if in_subfolder:
            parent_folder = os.path.basename(os.path.dirname(base_folder))  # Get the name of the parent folder
            grandparent_folder = os.path.basename(os.path.dirname(os.path.dirname(base_folder)))  # Get the name of the grandparent folder
        else:
            parent_folder = base_folder_name  # Use base folder as parent
            grandparent_folder = os.path.basename(os.path.dirname(base_folder))  # Use parent as grandparent
        
        file_counts = {}  # Dictionary to count files by type

        # Count files by their extension using selected_files
        for file in selected_files:
            file_extension = os.path.splitext(file)[1]
            if file_extension not in file_counts:
                file_counts[file_extension] = 0
            file_counts[file_extension] += 1

        # Rename files based on the new naming convention using selected_files
        for file_extension, count in file_counts.items():
            increment = 1  # Reset increment for each file type
            num_digits = 4  # Determine the number of digits needed

            # Get files of current extension and sort them
            current_extension_files = [f for f in selected_files if os.path.splitext(f)[1] == file_extension]
            print(current_extension_files)

            sorted_files = sort_files(current_extension_files)
            print(sorted_files)

            for file in sorted_files:
                new_file_name = f"{parent_folder}_{grandparent_folder}_{increment:0{num_digits}d}{file_extension}".replace("._","")
                
                # Rename the file (keeping it in the same folder)
                old_file_path = file
                new_file_path = os.path.join(os.path.dirname(file), new_file_name)
                
                os.rename(old_file_path, new_file_path)

                renamed_count += 1
                progress.set_text(f"Renaming {old_file_path} to {new_file_name}")
                progress.report_progress(renamed_count / total_files)

                increment += 1  # Increment for the next file of the same type

        progress.finish()
        ap.UI().show_success("Files Renamed Successfully", f"{renamed_count} files have been renamed.")

    except Exception as e:
        progress.finish()
        print(e)
        ap.UI().show_error("Error", "Open the console for more information")

def main():

    def button_clicked_cb(dialog):
        in_subfolder = dialog.get_value("skip_base_folder")
        ctx.run_async(batch_rename, selected_files, base_folder, in_subfolder)
        dialog.close()

    def checkbox_checked_cb(dialog,value):
        dialog.set_value("text_preview", create_preview(value))

    def create_preview(in_subfolder):
        if(in_subfolder):
            parent_folder = os.path.basename(os.path.dirname(base_folder))  # Get the name of the parent folder
            grandparent_folder = os.path.basename(os.path.dirname(os.path.dirname(base_folder))) 
            name_preview = parent_folder+"_"+grandparent_folder+"_0001"+file_extension
            return name_preview
        else:
            parent_folder = os.path.basename(os.path.dirname(base_folder))
            name_preview = os.path.basename(base_folder)+"_"+parent_folder+"_0001"+file_extension
            return name_preview

    ctx = ap.get_context() 

    selected_files = ctx.selected_files
    base_folder = os.path.dirname(ctx.path) 
    total_files = len(selected_files)
    file_extension = os.path.splitext(ctx.path)[1]

    

    dialog = ap.Dialog()
    dialog.title = "Rename Preview"
    dialog.add_checkbox(text="Files are in a subfolder",var="skip_base_folder",default=True,callback=checkbox_checked_cb)
    dialog.add_info("E.g. if your raw files ( e.g. .CR2,.NEF,.ARW) are in a folder called 'RAW'")
    dialog.add_empty()

    dialog.add_info("File batches are grouped by file extension. The new file name will look similar to this:")
    dialog.add_text(text=create_preview(True),var="text_preview")

    dialog.add_info(f"Continue to rename {total_files} files")
    dialog.add_button("Continue", callback=button_clicked_cb)
    dialog.show()    

if __name__ == "__main__":
    main()