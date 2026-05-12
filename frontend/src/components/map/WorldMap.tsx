import { useState } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
  ZoomableGroup,
} from "react-simple-maps";
import type { MapCountryData } from "@/types";

const GEO_URL =
  "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

// Country name → approximate [lon, lat] coordinates
const COUNTRY_COORDS: Record<string, [number, number]> = {
  "United States": [-100, 38],
  "United Kingdom": [-2, 54],
  Germany: [10, 51],
  France: [2, 46],
  Japan: [138, 36],
  China: [104, 35],
  India: [78, 22],
  Brazil: [-51, -14],
  Canada: [-96, 60],
  Australia: [134, -25],
  Russia: [100, 60],
  Singapore: [104, 1],
  Vietnam: [106, 16],
  "South Korea": [128, 37],
  Netherlands: [5, 52],
  "United Arab Emirates": [54, 24],
  Indonesia: [106, -6],
  Thailand: [101, 15],
  Malaysia: [110, 4],
  Philippines: [122, 12],
};

interface Props {
  data: MapCountryData[];
  loading: boolean;
}

export default function WorldMap({ data, loading }: Props) {
  const [tooltip, setTooltip] = useState<{
    x: number;
    y: number;
    item: MapCountryData;
  } | null>(null);

  const markers = data.filter((item) => COUNTRY_COORDS[item.country]);

  return (
    <div className="card p-5 relative">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">
        Server Distribution
      </h3>
      {loading ? (
        <div className="h-72 bg-slate-800/30 rounded-lg animate-pulse" />
      ) : (
        <div className="relative">
          <ComposableMap
            projectionConfig={{ scale: 147 }}
            style={{ width: "100%", height: "320px" }}
          >
            <ZoomableGroup center={[0, 10]}>
              <Geographies geography={GEO_URL}>
                {({ geographies }) =>
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  geographies.map((geo: any) => (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      fill="#1e293b"
                      stroke="#334155"
                      strokeWidth={0.5}
                      style={{
                        default: { outline: "none" },
                        hover: { fill: "#2d3f55", outline: "none" },
                        pressed: { outline: "none" },
                      }}
                    />
                  ))
                }
              </Geographies>
              {markers.map((item) => {
                const coords = COUNTRY_COORDS[item.country]!;
                const isLarge = item.count > 5;
                return (
                  <Marker
                    key={item.country}
                    coordinates={coords}
                    onMouseEnter={(e: React.MouseEvent) => {
                      setTooltip({ x: e.clientX, y: e.clientY, item });
                    }}
                    onMouseLeave={() => setTooltip(null)}
                  >
                    <circle
                      r={isLarge ? 8 : Math.max(4, item.count * 1.5)}
                      fill="#3b82f6"
                      fillOpacity={0.7}
                      stroke="#60a5fa"
                      strokeWidth={1.5}
                      className="cursor-pointer"
                    />
                    {item.count > 1 && (
                      <text
                        textAnchor="middle"
                        y={4}
                        style={{
                          fontSize: 8,
                          fill: "white",
                          fontWeight: "bold",
                          pointerEvents: "none",
                        }}
                      >
                        {item.count}
                      </text>
                    )}
                  </Marker>
                );
              })}
            </ZoomableGroup>
          </ComposableMap>

          {/* Tooltip */}
          {tooltip && (
            <div
              className="fixed z-50 card p-3 text-xs pointer-events-none shadow-xl"
              style={{ left: tooltip.x + 12, top: tooltip.y - 8 }}
            >
              <p className="font-semibold text-white mb-1">
                {tooltip.item.country}
              </p>
              <p className="text-slate-400 mb-2">
                {tooltip.item.count} server(s)
              </p>
              {tooltip.item.servers.slice(0, 3).map((s) => (
                <div key={s.id} className="flex items-center gap-2 py-0.5">
                  <span
                    className={`w-1.5 h-1.5 rounded-full ${s.status === "Online" ? "bg-emerald-400" : "bg-red-400"}`}
                  />
                  <span className="text-slate-300">{s.name}</span>
                  <span className="text-slate-500">{s.ip_address}</span>
                </div>
              ))}
              {tooltip.item.servers.length > 3 && (
                <p className="text-slate-600 mt-1">
                  +{tooltip.item.servers.length - 3} more
                </p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Legend */}
      <div className="flex items-center gap-4 mt-3">
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-blue-500" />
          <span className="text-xs text-slate-500">Server cluster</span>
        </div>
        <span className="text-xs text-slate-600">{data.length} countries</span>
      </div>
    </div>
  );
}
