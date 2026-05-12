import { useState } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
  ZoomableGroup,
} from "react-simple-maps";
import type { MapCountryData } from "@/types";

const GEO_URL = "/countries-110m.json";

// Country name → approximate [lon, lat] coordinates
const COUNTRY_COORDS: Record<string, [number, number]> = {
  Afghanistan: [67, 33],
  Albania: [20, 41],
  Algeria: [3, 28],
  Andorra: [1.5, 42.5],
  Angola: [18, -12],
  Argentina: [-64, -34],
  Armenia: [45, 40],
  Australia: [134, -25],
  Austria: [14, 47],
  Azerbaijan: [47.5, 40.5],
  Bahrain: [50.5, 26],
  Bangladesh: [90, 24],
  Belarus: [28, 53],
  Belgium: [4, 50.8],
  Belize: [-88.7, 17.2],
  Benin: [2.3, 9.3],
  Bhutan: [90.4, 27.5],
  Bolivia: [-65, -17],
  "Bosnia and Herzegovina": [17.7, 44.2],
  Botswana: [24, -22],
  Brazil: [-51, -14],
  Brunei: [114.7, 4.5],
  Bulgaria: [25, 43],
  "Burkina Faso": [-2, 13],
  Burundi: [29.9, -3.4],
  Cambodia: [105, 12.5],
  Cameroon: [12.3, 5.7],
  Canada: [-96, 60],
  "Central African Republic": [21, 7],
  Chad: [18.7, 15.5],
  Chile: [-71, -30],
  China: [104, 35],
  Colombia: [-74, 4],
  "Congo (DRC)": [25, -3],
  "Costa Rica": [-84, 10],
  Croatia: [15.5, 45.1],
  Cuba: [-80, 22],
  Cyprus: [33, 35],
  "Czech Republic": [15.5, 49.8],
  Denmark: [10, 56],
  Djibouti: [43, 11.8],
  "Dominican Republic": [-70.2, 18.9],
  Ecuador: [-77.8, -1.8],
  Egypt: [30, 27],
  "El Salvador": [-88.9, 13.8],
  Estonia: [25, 59],
  Ethiopia: [40, 8],
  Finland: [26, 64],
  France: [2, 46],
  Gabon: [11.8, -1],
  Georgia: [43.5, 42],
  Germany: [10, 51],
  Ghana: [-1, 8],
  Greece: [22, 39],
  Guatemala: [-90.2, 15.8],
  Guinea: [-11.8, 11],
  Haiti: [-73, 19],
  Honduras: [-86.6, 15],
  Hungary: [19, 47],
  Iceland: [-19, 65],
  India: [78, 22],
  Indonesia: [106, -6],
  Iran: [53, 32],
  Iraq: [44, 33],
  Ireland: [-8, 53],
  Israel: [34.8, 31.5],
  Italy: [12, 42],
  Jamaica: [-77.3, 18.1],
  Japan: [138, 36],
  Jordan: [37, 31],
  Kazakhstan: [68, 48],
  Kenya: [38, 1],
  Kuwait: [47.7, 29.3],
  Kyrgyzstan: [75, 41],
  Laos: [103, 18],
  Latvia: [25, 57],
  Lebanon: [35.8, 33.9],
  Libya: [17, 27],
  Lithuania: [24, 56],
  Luxembourg: [6.1, 49.8],
  Madagascar: [47, -20],
  Malaysia: [110, 4],
  Mali: [-2, 17],
  Malta: [14.4, 35.9],
  Mauritania: [-11, 20],
  Mexico: [-102, 24],
  Moldova: [29, 47],
  Mongolia: [105, 46],
  Morocco: [-5, 32],
  Mozambique: [35, -18],
  Myanmar: [96, 17],
  Namibia: [18, -22],
  Nepal: [84, 28],
  Netherlands: [5, 52],
  "New Zealand": [172, -41],
  Nicaragua: [-85, 13],
  Niger: [8, 16],
  Nigeria: [8, 10],
  "North Korea": [127, 40],
  "North Macedonia": [21.7, 41.6],
  Norway: [10, 62],
  Oman: [57, 22],
  Pakistan: [70, 30],
  Panama: [-80, 9],
  Paraguay: [-58, -23],
  Peru: [-76, -10],
  Philippines: [122, 12],
  Poland: [20, 52],
  Portugal: [-8, 39.5],
  Qatar: [51.2, 25.4],
  Romania: [25, 46],
  Russia: [100, 60],
  Rwanda: [30, -2],
  "Saudi Arabia": [45, 25],
  Senegal: [-14, 14],
  Serbia: [21, 44],
  Singapore: [104, 1],
  Slovakia: [19.5, 48.7],
  Slovenia: [15, 46],
  Somalia: [46, 6],
  "South Africa": [25, -29],
  "South Korea": [128, 37],
  "South Sudan": [31, 7],
  Spain: [-4, 40],
  "Sri Lanka": [81, 7],
  Sudan: [30, 15],
  Sweden: [18, 62],
  Switzerland: [8, 47],
  Syria: [38, 35],
  Taiwan: [121, 24],
  Tajikistan: [71, 39],
  Tanzania: [35, -6],
  Thailand: [101, 15],
  Tunisia: [9, 34],
  Turkey: [35, 39],
  Turkmenistan: [59, 40],
  Uganda: [32, 1],
  Ukraine: [32, 49],
  "United Arab Emirates": [54, 24],
  "United Kingdom": [-2, 54],
  "United States": [-100, 38],
  Uruguay: [-56, -33],
  Uzbekistan: [64, 41],
  Venezuela: [-66, 8],
  Vietnam: [106, 16],
  Yemen: [48, 15],
  Zambia: [28, -14],
  Zimbabwe: [30, -20],
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
