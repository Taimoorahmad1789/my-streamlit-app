import React,

{useState}
from

'react';
import

{Heart, AlertCircle, CheckCircle, TrendingUp, Zap, Activity}
from

'lucide-react';

export
default
function
CardiacDashboard()
{
    const[formData, setFormData] = useState({
    age: 45,
    gender: 'Male',
    chest_pain_type: 'Typical Angina',
    resting_blood_pressure: 120,
    cholesterol: 200,
    fasting_blood_sugar: 'False',
    resting_ecg: 'Normal',
    max_heart_rate: 150,
    exercise_induced_angina: 'No',
    st_depression: 0.0,
    st_slope: 'Upsloping'
});

const[results, setResults] = useState(null);
const[loading, setLoading] = useState(false);

const
handleInputChange = (field, value) = > {
    setFormData(prev= > ({...prev, [field]: value}));
};

const
generateReport = () = > {
    setLoading(true);

// Simulated
prediction
logic
setTimeout(() = > {
    const
riskScore = Math.random();
const
mockShapValues = {
    'max_heart_rate': -0.15,
    'age': 0.22,
    'cholesterol': 0.18,
    'st_depression': 0.14,
    'resting_blood_pressure': 0.08,
    'exercise_induced_angina': 0.06
};

setResults({
    riskScore,
    topFeature: 'age',
topNegativeFeature: 'max_heart_rate',
shapValues: mockShapValues
});
setLoading(false);
}, 1500);
};

const
getRiskStatus = (score) = > {
if (score > 0.7)
return {level: 'High Risk', color: 'from-red-500 to-red-600', icon: AlertCircle,
        message: 'Immediate medical consultation advised'};
if (
        score > 0.3) return {level: 'Moderate Risk', color: 'from-yellow-500 to-yellow-600', icon: TrendingUp, message: 'Regular monitoring recommended'};
return {level: 'Low Risk', color: 'from-green-500 to-green-600', icon: CheckCircle, message: 'Good cardiac health'};
};

const
risk = results ? getRiskStatus(results.riskScore): null;
const
RiskIcon = risk?.icon;

return (
    < div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" >
    {/ * Animated Background Elements * /}
    < div className="fixed inset-0 overflow-hidden pointer-events-none" >
    < div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500 opacity-5 rounded-full blur-3xl animate-pulse" > < / div >
    < div className="absolute bottom-0 right-1/4 w-96 h-96 bg-cyan-500 opacity-5 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}} > < / div >
    < / div >

    < div className="relative z-10" >
    {/ * Header * /}
    < header className="bg-gradient-to-r from-blue-600 to-cyan-600 shadow-2xl" >
    < div className="max-w-7xl mx-auto px-6 py-8" >
    < div className="flex items-center gap-4 mb-4" >
    < div className="bg-white p-3 rounded-lg shadow-lg" >
    < Heart className="text-red-500" size={32} / >
    < / div >
    < div >
    < h1 className="text-4xl font-bold text-white" > Cardiac Risk Assessment < / h1 >
    < p className="text-blue-100 mt-1" > AI-Powered Diagnostic Support System < / p >
    < / div >
    < / div >
    < / div >
    < / header >

    {/ * Main Content * /}
    < main className="max-w-7xl mx-auto px-6 py-12" >
    < div className="grid grid-cols-1 lg:grid-cols-3 gap-8" >
    {/ * Left Panel - Input Form * /}
    < div className="lg:col-span-1" >
    < div className="bg-white rounded-2xl shadow-2xl p-8 sticky top-8" >
    < h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2" >
    < Activity className="text-blue-600" / >
    Patient Data
    < / h2 >

    < div className="space-y-5" >
    {/ * Numerical Inputs * /}
    < div >
    < label className="block text-sm font-semibold text-gray-700 mb-2" > Age < / label >
    < input type="number" min="1" max="120" value={formData.age} onChange={(e) = > handleInputChange('age', parseInt(
    e.target.value))} className = "w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition" / >
                                  < / div >

                                      < div >
                                      < label
className = "block text-sm font-semibold text-gray-700 mb-2" > Resting
Blood
Pressure(mm
Hg) < / label >
        < input
type = "range"
min = "80"
max = "200"
value = {formData.resting_blood_pressure}
onChange = {(e) = > handleInputChange('resting_blood_pressure', parseInt(
    e.target.value))} className = "w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500" / >
                                  < div
className = "text-right text-sm font-semibold text-blue-600 mt-1" > {formData.resting_blood_pressure}
mm
Hg < / div >
       < / div >

           < div >
           < label
className = "block text-sm font-semibold text-gray-700 mb-2" > Cholesterol(mg / dl) < / label >
                                                                                        < input
type = "range"
min = "100"
max = "600"
value = {formData.cholesterol}
onChange = {(e) = > handleInputChange('cholesterol', parseInt(
    e.target.value))} className = "w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500" / >
                                  < div
className = "text-right text-sm font-semibold text-blue-600 mt-1" > {formData.cholesterol}
mg / dl < / div >
            < / div >

                < div >
                < label
className = "block text-sm font-semibold text-gray-700 mb-2" > Maximum
Heart
Rate < / label >
         < input
type = "range"
min = "60"
max = "220"
value = {formData.max_heart_rate}
onChange = {(e) = > handleInputChange('max_heart_rate', parseInt(
    e.target.value))} className = "w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500" / >
                                  < div
className = "text-right text-sm font-semibold text-blue-600 mt-1" > {formData.max_heart_rate}
bpm < / div >
        < / div >

            < div >
            < label
className = "block text-sm font-semibold text-gray-700 mb-2" > ST
Depression < / label >
               < input
type = "number"
min = "0"
max = "10"
step = "0.1"
value = {formData.st_depression}
onChange = {(e) = > handleInputChange('st_depression', parseFloat(
    e.target.value))} className = "w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition" / >
                                  < / div >

                                      { / * Categorical
Inputs * /}
< div >
  < label
className = "block text-sm font-semibold text-gray-700 mb-2" > Gender < / label >
                                                                          < select
value = {formData.gender}
onChange = {(e) = > handleInputChange('gender',
                                      e.target.value)} className = "w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition" >
                                                                   < option > Male < / option >
                                                                                       < option > Female < / option >
                                                                                                             < / select >
                                                                                                                 < / div >

                                                                                                                     < div >
                                                                                                                     < label
className = "block text-sm font-semibold text-gray-700 mb-2" > Chest
Pain
Type < / label >
         < select
value = {formData.chest_pain_type}
onChange = {(e) = > handleInputChange('chest_pain_type',
                                      e.target.value)} className = "w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition" >
                                                                   < option > Typical
Angina < / option >
           < option > Atypical
Angina < / option >
           < option > Non - anginal
Pain < / option >
         < option > Asymptomatic < / option >
                                     < / select >
                                         < / div >

                                             < div >
                                             < label
className = "block text-sm font-semibold text-gray-700 mb-2" > Fasting
Blood
Sugar > 120 < / label >
                < select
value = {formData.fasting_blood_sugar}
onChange = {(e) = > handleInputChange('fasting_blood_sugar',
                                      e.target.value)} className = "w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition" >
                                                                   < option > False < / option >
                                                                                        < option > True < / option >
                                                                                                            < / select >
                                                                                                                < / div >

                                                                                                                    < div >
                                                                                                                    < label
className = "block text-sm font-semibold text-gray-700 mb-2" > Resting
ECG
Results < / label >
            < select
value = {formData.resting_ecg}
onChange = {(e) = > handleInputChange('resting_ecg',
                                      e.target.value)} className = "w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition" >
                                                                   < option > Normal < / option >
                                                                                         < option > ST - T
Wave
Abnormality < / option >
                < option > Left
Ventricular
Hypertrophy < / option >
                < / select >
                    < / div >

                        < div >
                        < label
className = "block text-sm font-semibold text-gray-700 mb-2" > Exercise
Induced
Angina < / label >
           < select
value = {formData.exercise_induced_angina}
onChange = {(e) = > handleInputChange('exercise_induced_angina',
                                      e.target.value)} className = "w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition" >
                                                                   < option > No < / option >
                                                                                     < option > Yes < / option >
                                                                                                        < / select >
                                                                                                            < / div >

                                                                                                                < div >
                                                                                                                < label
className = "block text-sm font-semibold text-gray-700 mb-2" > ST
Slope < / label >
          < select
value = {formData.st_slope}
onChange = {(e) = > handleInputChange('st_slope',
                                      e.target.value)} className = "w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition" >
                                                                   < option > Upsloping < / option >
                                                                                            < option > Flat < / option >
                                                                                                                < option > Downsloping < / option >
                                                                                                                                           < / select >
                                                                                                                                               < / div >

                                                                                                                                                   < button
onClick = {generateReport}
disabled = {loading}
className = "w-full mt-8 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-bold py-3 rounded-lg transition transform hover:scale-105 active:scale-95 shadow-lg" >
            {loading ? 'Analyzing...': 'Generate Report'}
< / button >
    < / div >
        < / div >
            < / div >

                { / * Right
Panel - Results * /}
< div
className = "lg:col-span-2" >
            {results ? (
    < div className="space-y-6" >
    {/ * Risk Score Card * /}
    < div className={`bg-gradient-to-br ${risk.color} rounded-2xl shadow-2xl p-8 text-white transform transition hover:scale-105`} >
    < div className="flex items-center justify-between mb-6" >
    < h2 className="text-3xl font-bold" > Risk Assessment < / h2 >
    < RiskIcon size={48} className="opacity-80" / >
    < / div >
    < div className="mb-6" >
    < div className="text-6xl font-bold mb-2" > {Math.round(results.riskScore * 100)} % < / div >
                                                                                            < p
className = "text-xl font-semibold opacity-90" > Risk
Score < / p >
          < / div >
              < div
className = "w-full bg-white bg-opacity-30 rounded-full h-3 overflow-hidden" >
            < div
className = "bg-white h-full rounded-full transition-all duration-1000"
style = {{width: `${results.riskScore * 100} % `}} > < / div >
                                                         < / div >
                                                             < div
className = "mt-6 p-4 bg-white bg-opacity-20 rounded-lg" >
            < p
className = "text-lg font-semibold" > {risk.level} < / p >
                                                       < p
className = "text-sm opacity-90 mt-1" > {risk.message} < / p >
                                                           < / div >
                                                               < / div >

                                                                   { / * AI
Insights * /}
< div
className = "bg-white rounded-2xl shadow-2xl p-8" >
            < h3
className = "text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2" >
            < Zap
className = "text-yellow-500" / >
            AI
Insights
< / h3 >
    < div
className = "bg-gradient-to-r from-blue-50 to-cyan-50 p-6 rounded-lg border-l-4 border-blue-500" >
            < p
className = "text-gray-700 leading-relaxed" >
            AI
Analysis
shows
that < span
className = "font-bold text-blue-600" > age < / span > is a
major
contributor
to
this
risk
score.However, < span
className = "font-bold text-green-600" > maximum
heart
rate < / span > is helping
to
keep
the
overall
risk
assessment
lower.
< / p >
    < / div >
        < / div >

            { / * Feature
Impact * /}
< div
className = "bg-white rounded-2xl shadow-2xl p-8" >
            < h3
className = "text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2" >
            < TrendingUp
className = "text-cyan-600" / >
            Feature
Impact
Analysis
< / h3 >
    < div
className = "space-y-4" >
            {Object.entries(results.shapValues).sort((a, b) = > Math.abs(b[1]) - Math.abs(a[1])).map(
    ([feature, value]) = > (
    < div key={feature} >
    < div className="flex justify-between mb-2" >
    < span className="font-semibold text-gray-700 capitalize" > {feature.replace( / _ / g, ' ')} < / span >
                                                                                                     < span
className = {`font - bold ${value > 0 ? 'text-red-600': 'text-green-600'}`} > {value > 0 ? '+': ''}{value.toFixed(
    2)} < / span >
            < / div >
                < div
className = "w-full bg-gray-200 rounded-full h-2 overflow-hidden" >
            < div
className = {`h - full
rounded - full
transition - all ${value > 0 ? 'bg-red-500': 'bg-green-500'}`}
style = {{width: `${Math.abs(value) * 100} % `}}
> < / div >
      < / div >
          < / div >
))}
< / div >
    < / div >
        < / div >
): (
    < div className="bg-white rounded-2xl shadow-2xl p-16 flex items-center justify-center min-h-96" >
    < div className="text-center" >
    < div className="bg-blue-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6" >
    < Heart className="text-blue-600" size={48} / >
    < / div >
    < h3 className="text-2xl font-bold text-gray-800 mb-2" > Ready for Analysis < / h3 >
    < p className="text-gray-600" > Enter patient data on the left and click "Generate Report" to see diagnostic insights.< / p >
    < / div >
    < / div >
)}
< / div >
    < / div >
        < / main >

            { / * Footer * /}
< footer
className = "bg-gray-900 border-t border-gray-800 py-8 mt-16" >
            < div
className = "max-w-7xl mx-auto px-6 text-center text-gray-400" >
            < p >🏥 Cardiac
Risk
Assessment
Dashboard
v1
.0 | Professional
Medical
Support
Tool < / p >
         < p
className = "text-sm mt-2" > Disclaimer: This
tool
provides
diagnostic
support
only.Always
consult
qualified
healthcare
professionals. < / p >
                   < / div >
                       < / footer >
                           < / div >
                               < / div >
);
}