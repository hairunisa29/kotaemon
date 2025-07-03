import gradio as gr
import os
from ktem.app import BasePage
from ktem.db.engine import engine
from sqlalchemy.orm import Session

class FileList(BasePage):
    def __init__(self, app, index):
        self._app = app
        self.on_building_ui()
        self._index = index

    def on_building_ui(self):
        self.container = gr.HTML(visible=True)

    def update(self, file_ids):
        print("FILE LIST", file_ids)
        index = self._index

        if not file_ids:
            return gr.update(value="<div>No files found.</div>")

        Source = index._resources["Source"]
        with Session(engine) as session:
            files = session.query(Source).filter(Source.id.in_(file_ids)).all()

            file_dicts = []

            for file in files:
                file_dicts.append({
                    "id": file.id,
                    "name": file.name,
                    "path": f"ktem_app_data/gradio_tmp/{os.path.basename(file.path)}" if file.path else "",
                    "date_created": file.date_created.strftime("%d/%m/%Y") if file.date_created else "",
                    "date_from_file_name": file.date_from_file_name.strftime("%d/%m/%Y") if file.date_from_file_name else "",
                    "date_from_content": file.date_from_content.strftime("%d/%m/%Y") if file.date_from_content else "",
                })
            
            print("PRINT FILE DICTS INSIDE FILE LIST", file_dicts)

            if not file_dicts:
                return gr.update(value="<div>No files found.</div>")
            cards = []
            for file in file_dicts:
                display_date = (
                    file["date_from_file_name"]
                    or file["date_from_content"]
                    or file["date_created"]
                )

                cards.append(f"""
                    <div style="border:1px solid #bbb; border-radius:8px; padding:10px; margin-bottom:10px; display:flex; flex-direction:column; gap:8px; max-width:320px;">
                        <div style="font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                            {file["name"]}
                        </div>
                        <div style="display:flex; align-items:center; gap:6px; color:#555;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="vertical-align:middle;"><rect x="3" y="4" width="18" height="18" rx="2" fill="#eee" stroke="#bbb"/><rect x="7" y="10" width="10" height="8" rx="1" fill="#fff" stroke="#bbb"/><rect x="7" y="2" width="2" height="4" rx="1" fill="#bbb"/><rect x="15" y="2" width="2" height="4" rx="1" fill="#bbb"/></svg>
                            <span style="font-size:0.95em;">{display_date}</span>
                        </div>
                        <button style="align-self:flex-end; background:#fff; border:1px solid #bbb; border-radius:5px; padding:3px 12px; cursor:pointer; display:flex; align-items:center; gap:4px;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#888" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="#888"/></svg>
                            show
                        </button>
                    </div>
                    """)
            return gr.update(value="".join(cards))
