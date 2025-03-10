import anchorpoint as ap
import os

def batch_rename(selected_files, base_folder):
    progress = ap.Progress("Renaming Files", infinite=False)
    progress.set_cancelable(True)

    total_files = len(selected_files)
    renamed_count = 0

    try:
        base_folder_name = os.path.basename(base_folder)  # Get the name of the base folder
        parent_folder = os.path.basename(os.path.dirname(base_folder))  # Get the name of the parent folder
        grandparent_folder = os.path.basename(os.path.dirname(os.path.dirname(base_folder)))  # Get the name of the grandparent folder
        file_counts = {}  # Dictionary to count files by type

        # Count files by their extension
        for root, _, files in os.walk(base_folder):
            for file in files:
                file_extension = os.path.splitext(file)[1]
                if file_extension not in file_counts:
                    file_counts[file_extension] = 0
                file_counts[file_extension] += 1

        # Rename files based on the new naming convention
        for file_extension, count in file_counts.items():
            increment = 1  # Reset increment for each file type
            num_digits = len(str(count))  # Determine the number of digits needed

            for root, _, files in os.walk(base_folder):
                for file in files:
                    if os.path.splitext(file)[1] == file_extension:
                        new_file_name = f"{parent_folder}_{grandparent_folder}_{increment:0{num_digits}d}{file_extension}".replace("._","")
                        
                        # Rename the file (keeping it in the same folder)
                        old_file_path = os.path.join(root, file)
                        new_file_path = os.path.join(root, new_file_name)
                        
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
        ctx.run_async(batch_rename, selected_files,base_folder)
        dialog.close()

    def checkbox_checked_cb(dialog,value):
        dialog.set_value("text_preview", create_preview(value))

    def create_preview(in_subfolder):
        if(in_subfolder):
            parent_folder = os.path.basename(os.path.dirname(base_folder))  # Get the name of the parent folder
            grandparent_folder = os.path.basename(os.path.dirname(os.path.dirname(base_folder))) 
            name_preview = parent_folder+"_"+grandparent_folder+"_"+digits+"1"+file_extension
            return name_preview
        else:
            parent_folder = os.path.basename(os.path.dirname(base_folder))
            name_preview = os.path.basename(base_folder)+"_"+parent_folder+"_"+digits+"1"+file_extension
            return name_preview

    ctx = ap.get_context() 

    selected_files = ctx.selected_files
    base_folder = os.path.dirname(ctx.path) 
    total_files = len(selected_files)
    digits = "0" * (len(str(total_files)) - 1)
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