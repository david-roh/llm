import Neo4jLogoBW from '../../logo.svg';
import Neo4jLogoColor from '../../logo-color.svg';
import {
  MoonIconOutline,
  SunIconOutline,
  CodeBracketSquareIconOutline,
  InformationCircleIconOutline,
} from '@neo4j-ndl/react/icons';
import { Typography } from '@neo4j-ndl/react';
import { memo, useCallback, useContext, useEffect } from 'react';
import { IconButtonWithToolTip } from '../UI/IconButtonToolTip';
import { tooltips } from '../../utils/Constants';
import { useFileContext } from '../../context/UsersFiles';
import { ThemeWrapperContext } from '../../context/ThemeWrapper';

function Header() {
  const { colorMode, toggleColorMode } = useContext(ThemeWrapperContext);
  const { isSchema, setIsSchema } = useFileContext();

  const handleURLClick = useCallback((url: string) => {
    window.open(url, '_blank');
  }, []);

  useEffect(() => {
    setIsSchema(isSchema);
  }, [isSchema]);

  return (
    <header className="sticky top-0 z-50 w-full backdrop-blur-md">
      <div 
        className="border-b border-opacity-20"
        style={{ 
          background: colorMode === 'dark' 
            ? 'rgba(23, 23, 23, 0.8)' 
            : 'rgba(255, 255, 255, 0.8)',
          borderColor: `rgb(var(--theme-palette-neutral-border-weak))`
        }}
      >
        <nav
          className="mx-auto max-w-[1920px] px-4 py-3"
          role="navigation"
          data-testid="navigation"
          id="navigation"
          aria-label="main navigation"
        >
          <div className="flex items-center justify-between">
            {/* Logo Section */}
            <div className="flex items-center space-x-4">
              <Typography 
                variant="h6" 
                component="a" 
                href="#" 
                className="flex items-center group"
              >
                <img
                  src={colorMode === 'dark' ? Neo4jLogoBW : Neo4jLogoColor}
                  className="h-8 transition-transform duration-200 group-hover:scale-105"
                  alt="Neo4j Logo"
                />
              </Typography>
            </div>

            {/* Actions Section */}
            <div className="flex items-center">
              <div className={`
                flex items-center gap-2 rounded-full px-3 py-1.5
                ${colorMode === 'dark' ? 'bg-gray-800/50' : 'bg-gray-100/50'}
                transition-colors duration-300
              `}>
                {/* Documentation Button */}
                <IconButtonWithToolTip
                  text={tooltips.documentation}
                  onClick={() => handleURLClick('https://neo4j.com/labs/genai-ecosystem/llm-graph-builder')}
                  size="large"
                  clean
                  placement="left"
                  label={tooltips.documentation}
                  className={`
                    rounded-full p-2
                    transition-all duration-200
                    hover:bg-opacity-10 hover:scale-105
                    active:scale-95
                    ${colorMode === 'dark' ? 'hover:bg-white' : 'hover:bg-gray-900'}
                  `}
                >
                  <InformationCircleIconOutline className="w-5 h-5" />
                </IconButtonWithToolTip>

                {/* GitHub Button */}
                <IconButtonWithToolTip
                  label={tooltips.github}
                  onClick={() => handleURLClick('https://github.com/neo4j-labs/llm-graph-builder/issues')}
                  text={tooltips.github}
                  size="large"
                  clean
                  className={`
                    rounded-full p-2
                    transition-all duration-200
                    hover:bg-opacity-10 hover:scale-105
                    active:scale-95
                    ${colorMode === 'dark' ? 'hover:bg-white' : 'hover:bg-gray-900'}
                  `}
                >
                  <CodeBracketSquareIconOutline className="w-5 h-5" />
                </IconButtonWithToolTip>

                {/* Theme Toggle Button */}
                <IconButtonWithToolTip
                  label={tooltips.theme}
                  text={tooltips.theme}
                  clean
                  size="large"
                  onClick={toggleColorMode}
                  placement="left"
                  className={`
                    rounded-full p-2
                    transition-all duration-200
                    hover:bg-opacity-10 hover:scale-105
                    active:scale-95
                    ${colorMode === 'dark' ? 'hover:bg-white' : 'hover:bg-gray-900'}
                  `}
                >
                  {colorMode === 'dark' ? (
                    <span role="img" aria-label="sun" className="animate-fade-in">
                      <SunIconOutline className="w-5 h-5" />
                    </span>
                  ) : (
                    <span role="img" aria-label="moon" className="animate-fade-in">
                      <MoonIconOutline className="w-5 h-5" />
                    </span>
                  )}
                </IconButtonWithToolTip>
              </div>
            </div>
          </div>
        </nav>
      </div>
    </header>
  );
}
export default memo(Header);

