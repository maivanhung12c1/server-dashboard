import { X } from "lucide-react";
import { useEffect, useState } from "react";
import type { CreateServerPayload, Server } from "@/types";

interface Props {
  server?: Server | null;
  onClose: () => void;
  onSubmit: (data: CreateServerPayload) => Promise<void>;
}

const EMPTY_FORM: CreateServerPayload = {
  name: "",
  ip_address: "",
  country: "",
  os: "",
  os_version: "",
  platform: "",
  arch: "x86_64",
  status: "Online",
};

export default function ServerForm({ server, onClose, onSubmit }: Props) {
  const [form, setForm] = useState<CreateServerPayload>(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (server) {
      setForm({
        name: server.name,
        ip_address: server.ip_address,
        country: server.country,
        os: server.os,
        os_version: server.os_version,
        platform: server.platform,
        arch: server.arch,
        status: server.status,
      });
    } else {
      setForm(EMPTY_FORM);
    }
    setError(null);
  }, [server]);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError(null);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await onSubmit(form);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setSubmitting(false);
    }
  }

  const FIELDS: {
    name: keyof CreateServerPayload;
    label: string;
    placeholder: string;
    type?: string;
  }[] = [
    { name: "name", label: "Server Name", placeholder: "web-server-01" },
    { name: "ip_address", label: "IP Address", placeholder: "192.168.1.10" },
    { name: "country", label: "Country", placeholder: "Vietnam" },
    { name: "os", label: "OS", placeholder: "Ubuntu" },
    { name: "os_version", label: "OS Version", placeholder: "22.04 LTS" },
    { name: "platform", label: "Platform", placeholder: "Nginx" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      {/* Backdrop click to close */}
      <div className="absolute inset-0" onClick={onClose} />

      <div className="card w-full max-w-lg mx-4 shadow-2xl relative z-10">
        <div className="flex items-center justify-between p-5 border-b border-slate-700/50">
          <h2 className="text-sm font-semibold text-white">
            {server ? "Edit Server" : "Add New Server"}
          </h2>
          <button
            onClick={onClose}
            className="p-1 text-slate-500 hover:text-white hover:bg-slate-700 rounded transition-colors"
          >
            <X size={15} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div className="grid grid-cols-2 gap-3">
            {FIELDS.map(({ name, label, placeholder }) => (
              <div key={name}>
                <label className="text-xs text-slate-400 mb-1.5 block">
                  {label} *
                </label>
                <input
                  name={name}
                  required
                  value={form[name] as string}
                  onChange={handleChange}
                  className="input"
                  placeholder={placeholder}
                />
              </div>
            ))}
            <div>
              <label className="text-xs text-slate-400 mb-1.5 block">
                Architecture *
              </label>
              <select
                name="arch"
                value={form.arch}
                onChange={handleChange}
                className="select"
              >
                <option value="x86_64">x86_64</option>
                <option value="ARM64">ARM64</option>
                <option value="ARM">ARM</option>
                <option value="x86">x86</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1.5 block">
                Status
              </label>
              <select
                name="status"
                value={form.status}
                onChange={handleChange}
                className="select"
              >
                <option value="Online">Online</option>
                <option value="Offline">Offline</option>
              </select>
            </div>
          </div>

          {error && (
            <div className="px-3 py-2 bg-red-500/10 border border-red-500/20 rounded-lg">
              <p className="text-xs text-red-400">{error}</p>
            </div>
          )}

          <div className="flex justify-end gap-3 pt-1">
            <button type="button" onClick={onClose} className="btn-ghost">
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="btn-primary disabled:opacity-50"
            >
              {submitting
                ? "Saving..."
                : server
                  ? "Save Changes"
                  : "Create Server"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
