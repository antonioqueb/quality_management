/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const IMAGE_EXTS = ["jpg", "jpeg", "png", "gif", "webp", "bmp", "svg"];
const VIDEO_EXTS = ["mp4", "webm", "ogg", "mov", "avi", "mkv"];
const PDF_EXTS = ["pdf"];

function getFileExtension(filename) {
    if (!filename) return "";
    return (filename.split(".").pop() || "").toLowerCase();
}

function getFileType(filename) {
    const ext = getFileExtension(filename);
    if (IMAGE_EXTS.includes(ext)) return "image";
    if (VIDEO_EXTS.includes(ext)) return "video";
    if (PDF_EXTS.includes(ext)) return "pdf";
    return "other";
}

export class EvidenceViewerWidget extends Component {
    static template = "quality_management.EvidenceViewerWidget";
    static props = { ...standardFieldProps };

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            attachments: [],
            loading: true,
            lightbox: null,  // { type, url, name }
        });
        this._loadAttachments();
        onWillUpdateProps(() => this._loadAttachments());
    }

    get recordIds() {
        const val = this.props.record.data[this.props.name];
        if (!val) return [];
        if (val.records) return val.records.map((r) => r.resId);
        if (val.currentIds) return val.currentIds;
        return [];
    }

    async _loadAttachments() {
        this.state.loading = true;
        const ids = this.recordIds;
        if (!ids.length) {
            this.state.attachments = [];
            this.state.loading = false;
            return;
        }
        try {
            const attachments = await this.orm.read("ir.attachment", ids, [
                "name", "mimetype", "datas", "type", "url",
            ]);
            this.state.attachments = attachments.map((att) => {
                const fileType = getFileType(att.name);
                let src = "";
                if (att.type === "url" && att.url) {
                    src = att.url;
                } else if (att.datas) {
                    const mime = att.mimetype || "application/octet-stream";
                    src = `data:${mime};base64,${att.datas}`;
                } else {
                    src = `/web/content/${att.id}?download=false`;
                }
                return {
                    id: att.id,
                    name: att.name,
                    mimetype: att.mimetype,
                    fileType,
                    src,
                    downloadUrl: `/web/content/${att.id}?download=true`,
                };
            });
        } catch (e) {
            console.error("EvidenceViewer: error loading attachments", e);
            this.state.attachments = [];
        }
        this.state.loading = false;
    }

    openLightbox(att) {
        if (att.fileType === "image" || att.fileType === "video" || att.fileType === "pdf") {
            this.state.lightbox = att;
        }
    }

    closeLightbox() {
        this.state.lightbox = null;
    }

    onLightboxBackdrop(ev) {
        if (ev.target === ev.currentTarget) {
            this.closeLightbox();
        }
    }
}

EvidenceViewerWidget.template = "quality_management.EvidenceViewerWidget";

registry.category("fields").add("evidence_viewer", {
    component: EvidenceViewerWidget,
    supportedTypes: ["many2many"],
});