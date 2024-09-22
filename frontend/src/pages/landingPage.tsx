import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Hero from '../components/Hero';
import LogoCollection from '../components/LogoCollection';
import Features from '../components/Features';
import FAQ from '../components/FAQ';
import Footer from '../components/Footer';


export default function LandingPage() {
    return (
        <>
            <Hero />
            <Box sx={{ bgcolor: 'background.default' }}>
                <LogoCollection />
                <Features />
                <Divider />
                <FAQ />
                <Divider />
                <Footer />
            </Box>
        </>
    );
}